#!/usr/bin/env python3
"""Generate a photo-treatment scene (1920x1080) for the documentary pipeline.

Takes a real photograph (archival / Commons) and produces a scene with:
  - cold colour grade (CSS filter + tint overlays)
  - slow push-in / drift (closed-form function of t, deterministic)
  - two-layer snowfall (far + near flakes = depth parallax over the photo)
  - film grain (shared core engine)
  - optional typed lower-third (phone-large text, holds >= 2 s)

The generated HTML expects the shared engine at ../assets/ (core.js, core.css,
gsap.min.js) relative to the scene file — the standard prod2 layout.

Usage:
  python3 make_photo_scene.py --photo crash_site.jpg --out sceneA_flash.html \
      --id sceneA_flash --duration 2.2 --imgw 2060 --left -70 --top -215 \
      --scale0 1.02 --scale1 1.09 --origin "46% 40%"
  Add --title "THE ANDES — 13 OCTOBER 1972" --subtitle "..." for a lower-third.
"""
import argparse, os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--photo', required=True)       # path relative to scene file
    ap.add_argument('--out', required=True)
    ap.add_argument('--id', required=True)
    ap.add_argument('--duration', type=float, required=True)
    ap.add_argument('--imgw', type=int, default=2060)   # displayed image width (px)
    ap.add_argument('--left', type=int, default=-70)
    ap.add_argument('--top', type=int, default=-215)
    ap.add_argument('--scale0', type=float, default=1.02)
    ap.add_argument('--scale1', type=float, default=1.09)
    ap.add_argument('--dx', type=float, default=0)      # extra x drift px over scene
    ap.add_argument('--dy', type=float, default=0)
    ap.add_argument('--origin', default='50% 42%')
    ap.add_argument('--title', default='')
    ap.add_argument('--subtitle', default='')
    ap.add_argument('--ltbottom', type=int, default=104)  # lower-third bottom offset (raise to clear the caption band)
    ap.add_argument('--fadein', type=float, default=0.3)
    a = ap.parse_args()

    lt = ''
    if a.title:
        lt = f'''<div id="lt">
    <div id="ltRule"></div>
    <div id="ltTitle"><span id="ltText"></span><span id="ltCaret"></span></div>
    <div id="ltSub">{a.subtitle}</div>
  </div>'''
    html = TEMPLATE.replace('__PHOTO__', a.photo) \
        .replace('__ID__', a.id).replace('__DUR__', str(a.duration)) \
        .replace('__IMGW__', str(a.imgw)).replace('__LEFT__', str(a.left)) \
        .replace('__TOP__', str(a.top)).replace('__S0__', str(a.scale0)) \
        .replace('__S1__', str(a.scale1)).replace('__DX__', str(a.dx)) \
        .replace('__DY__', str(a.dy)).replace('__ORIGIN__', a.origin) \
        .replace('__FADEIN__', str(a.fadein)) \
        .replace('__TITLE__', a.title).replace('__LT__', lt) \
        .replace('__LTBOTTOM__', str(a.ltbottom)) \
        .replace('__HASLT__', '1' if a.title else '0')
    with open(a.out, 'w') as f:
        f.write(html)
    print('wrote', a.out)

TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Scene — photo treatment</title>
<link rel="stylesheet" href="../assets/core.css">
<style>
  #stage { background: #04070c; }
  #photoWrap { position: absolute; inset: 0; overflow: hidden; opacity: 1; }
  #photo { position: absolute; left: __LEFT__px; top: __TOP__px; width: __IMGW__px;
    transform-origin: __ORIGIN__;
    filter: saturate(.52) contrast(1.08) brightness(.8) hue-rotate(-10deg); }
  #grade { position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(16,32,54,.30) 0%, rgba(10,20,36,.06) 34%,
                rgba(6,10,18,.12) 62%, rgba(3,6,11,.58) 100%); }
  #coldTint { position: absolute; inset: 0; background: rgba(38,74,120,.10); mix-blend-mode: overlay; }
  .snowCv { position: fixed; inset: 0; width: 1920px; height: 1080px; pointer-events: none; }
  #snowNear { filter: blur(1.6px); opacity: .8; }
  /* lower third */
  #lt { position: absolute; left: 118px; bottom: __LTBOTTOM__px; z-index: 50; }
  #ltRule { height: 6px; width: 0; background: #ffb042; box-shadow: 0 0 14px rgba(255,150,30,.4); }
  #ltTitle { margin-top: 20px; font-size: 60px; letter-spacing: 3px; color: #eef4fa;
    text-shadow: 0 4px 26px rgba(0,0,0,.9); white-space: nowrap; }
  #ltCaret { display: inline-block; width: 30px; height: 52px; margin-left: 8px;
    background: #ffb042; vertical-align: -6px; }
  #ltSub { margin-top: 14px; font-family: 'DejaVu Sans', sans-serif; font-weight: 700;
    font-size: 34px; letter-spacing: 2.5px; color: #ffb042; opacity: 0;
    text-shadow: 0 3px 16px rgba(0,0,0,.9); }
</style>
</head>
<body>
<div id="stage">
  <div id="photoWrap">
    <img id="photo" src="__PHOTO__">
    <div id="grade"></div><div id="coldTint"></div>
  </div>
  <canvas class="snowCv" id="snowFar" width="1920" height="1080"></canvas>
  <canvas class="snowCv" id="snowNear" width="1920" height="1080"></canvas>
  __LT__
</div>
<canvas id="grain"></canvas>
<div id="vignette"></div>

<script>window.SCENE = { id: '__ID__', duration: __DUR__ };</script>
<script src="../assets/gsap.min.js"></script>
<script src="../assets/core.js"></script>
<script>
const S0 = __S0__, S1 = __S1__, DX = __DX__, DY = __DY__, DUR = __DUR__;
const FADEIN = __FADEIN__, HASLT = __HASLT__, TITLE = "__TITLE__";
const easeIO = (p) => p < .5 ? 2*p*p : 1 - Math.pow(-2*p + 2, 2)/2;
const clamp01 = (v) => Math.max(0, Math.min(1, v));
const photo = document.getElementById('photo');
const wrap = document.getElementById('photoWrap');
const snowFar = makeSnow(document.getElementById('snowFar'), 130, 5);
const snowNear = makeSnow(document.getElementById('snowNear'), 55, 9);
const ltText = document.getElementById('ltText'), ltCaret = document.getElementById('ltCaret');
const ltRule = document.getElementById('ltRule'), ltSub = document.getElementById('ltSub');

window.__onSeek = (t) => {
  const p = easeIO(clamp01(t / DUR));
  const s = S0 + (S1 - S0) * p;
  photo.style.transform = `translate(${DX * p}px, ${DY * p}px) scale(${s})`;
  wrap.style.opacity = '1';  // photo at full opacity from frame 0: hard cut in,
                              // never a fade from black (v2 QC: black frames at
                              // 0.0s and at the 13.0s cut). FADEIN kept for API compat.
  snowFar(t); snowNear(t * 1.65 + 40);
  if (HASLT) {
    const n = Math.max(0, Math.min(TITLE.length, Math.floor((t - 0.4) * 26)));
    ltText.textContent = TITLE.slice(0, n);
    ltRule.style.width = (430 * easeIO(clamp01((t - 0.35) / 0.4))) + 'px';
    ltCaret.style.opacity = (t >= 0.4 && t < 2.3 && (n < TITLE.length || (t * 2.2) % 1 < 0.62)) ? '1' : '0';
    if (ltSub) ltSub.style.opacity = String(clamp01((t - 1.7) / 0.4));
  }
  window.__grainLevel = 0.09;
};
window.__boot();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    main()
