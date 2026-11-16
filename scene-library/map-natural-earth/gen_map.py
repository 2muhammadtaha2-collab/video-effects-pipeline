#!/usr/bin/env python3
"""Generate a documentary route-map scene (1920x1080) from Natural Earth data.

Real geographic data only: coastline comes from Natural Earth (public domain),
projected equirectangularly. Cities / routes / crash point are real lon/lat
coordinates defined in CONFIG below — edit them per video, re-run, render with
the standard capture tool.

Usage: python3 gen_map.py <output.html>
Data:  ./data/ne_50m_land.geojson  (Natural Earth 1:50m land, public domain)
       https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'ne_50m_land.geojson')

# ---- projection: equirectangular, stage 1920x1080 ---------------------------
W, H = 1920, 1080
LON_C, LAT_C, S = -63.0, -24.0, 30.0            # centre + px per degree latitude
KX = S * math.cos(math.radians(LAT_C))          # px per degree longitude
def proj(lon, lat):
    return (W/2 + (lon - LON_C) * KX, H/2 + (LAT_C - lat) * S)

# ---- geography for this video (Andes / Flight 571) ---------------------------
CITIES = [  # name, lon, lat, pop_time(s, scene-local), label_side
    ("MONTEVIDEO", -56.16, -34.90, 0.6, "right"),
    ("MENDOZA",    -68.85, -32.89, 1.5, "right"),
    ("MALARGÜE",   -69.58, -35.48, 1.7, "left"),
    ("CURICÓ",     -71.24, -34.98, 1.9, "left"),
    ("SANTIAGO",   -70.67, -33.45, 2.1, "left"),
]
TURN  = (-70.53, -34.98)   # turned north here, 60-69 km east of Curicó (dossier)
CRASH = (-70.286, -34.765) # Glaciar de las Lágrimas, Argentina (dossier)
PLANNED = [(-56.16,-34.90), (-68.85,-32.89), (-69.58,-35.48), (-71.24,-34.98), (-70.67,-33.45)]
ACTUAL  = [(-56.16,-34.90), (-68.85,-32.89), (-69.58,-35.48), TURN, CRASH]
REGIONS = [("ARGENTINA", -66.5, -38.5), ("CHILE", -70.8, -30.6), ("URUGUAY", -56.3, -32.6),
           ("PACIFIC OCEAN", -79.5, -22.0), ("ATLANTIC OCEAN", -46.0, -33.0)]

# ---- build the coastline path ------------------------------------------------
def build_land_path():
    d = json.load(open(DATA))
    lon_min, lon_max = LON_C - (W/2)/KX - 1, LON_C + (W/2)/KX + 1
    lat_min, lat_max = LAT_C - (H/2)/S - 1, LAT_C + (H/2)/S + 1
    parts, kept = [], 0
    def ring_path(ring):
        nonlocal kept
        xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
        if max(xs) < lon_min or min(xs) > lon_max or max(ys) < lat_min or min(ys) > lat_max:
            return None
        out, last = [], None
        for lon, lat in ring:
            x, y = proj(lon, lat)
            if last is None or abs(x-last[0]) + abs(y-last[1]) >= 1.2:
                out.append(f"{x:.0f},{y:.0f}"); last = (x, y); kept += 1
        if len(out) < 3: return None
        return "M" + "L".join(out) + "Z"
    def walk(geom):
        if geom['type'] == 'Polygon':
            for r in geom['coordinates']:
                p = ring_path(r)
                if p: parts.append(p)
        elif geom['type'] == 'MultiPolygon':
            for poly in geom['coordinates']:
                for r in poly:
                    p = ring_path(r)
                    if p: parts.append(p)
    for f in d['features']:
        walk(f['geometry'])
    print(f"land path: {len(parts)} rings, {kept} points", file=sys.stderr)
    return "".join(parts)

def pts_attr(coords):
    return " ".join(f"{proj(lon,lat)[0]:.1f},{proj(lon,lat)[1]:.1f}" for lon, lat in coords)

def main():
    out_path = sys.argv[1]
    land = build_land_path()
    cities_js = json.dumps([{"name": n, "xy": proj(lon, lat), "pop": p, "side": s}
                            for n, lon, lat, p, s in CITIES])
    regions_js = json.dumps([{"name": n, "xy": proj(lon, lat)} for n, lon, lat in REGIONS])
    crash_xy = proj(*CRASH)
    html = TEMPLATE.replace("__LAND__", land) \
                   .replace("__PLANNED__", pts_attr(PLANNED)) \
                   .replace("__ACTUAL__", pts_attr(ACTUAL)) \
                   .replace("__CITIES__", cities_js) \
                   .replace("__REGIONS__", regions_js) \
                   .replace("__CRASH__", json.dumps(crash_xy))
    with open(out_path, 'w') as f:
        f.write(html)
    print("wrote", out_path, file=sys.stderr)

TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Scene — Natural Earth route map</title>
<link rel="stylesheet" href="../assets/core.css">
<style>
  #stage { background: linear-gradient(160deg, #081120 0%, #05090f 55%, #04070c 100%); }
  #mapSvg { position: absolute; inset: 0; }
  .land { fill: #1a2839; stroke: #4a6a8c; stroke-width: 1.6; }
  .grat { stroke: rgba(130,170,210,.08); stroke-width: 1; }
  #routePlan { fill: none; stroke: #a9c2d8; stroke-width: 3.4; stroke-dasharray: 9 8; opacity: .85; }
  #routeAct  { fill: none; stroke: #ffb042; stroke-width: 4.6; stroke-linecap: round;
               filter: drop-shadow(0 0 7px rgba(255,150,30,.45)); }
  #planeMark { fill: #ffd9a0; stroke: #201503; stroke-width: 1.4; }
  .ring { fill: none; stroke: #ff5347; stroke-width: 3; }
  #crashCoreSvg { fill: #ff5347; stroke: #ffd9d4; stroke-width: 1.6; }
  /* HTML overlay: positions recomputed per frame so text never scales */
  .ov { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; z-index: 40; }
  .city { position: absolute; transform: translate(-50%,-50%); opacity: 0; }
  .city .dot { position: absolute; left: -8px; top: -8px; width: 16px; height: 16px; border-radius: 50%;
    background: #e8f0f8; border: 2px solid #0a141f; box-shadow: 0 0 10px rgba(160,200,240,.55); }
  .city .lab { position: absolute; top: -19px; font-family: 'DejaVu Sans', sans-serif; font-weight: 700;
    font-size: 36px; letter-spacing: 1.5px; color: #dfe8f2; white-space: nowrap;
    text-shadow: 0 2px 10px rgba(0,0,0,.9), 0 0 26px rgba(0,0,0,.65); }
  .city .lab.right { left: 20px; } .city .lab.left { right: 20px; }
  .region { position: absolute; transform: translate(-50%,-50%); font-family: 'DejaVu Sans', sans-serif;
    font-weight: 700; font-size: 38px; letter-spacing: 9px; color: rgba(170,200,230,.34); white-space: nowrap; }
  .region.ocean { font-size: 34px; letter-spacing: 6px; font-style: italic; color: rgba(140,180,220,.26); }
  #callout { position: absolute; left: 1030px; top: 905px; width: 716px; padding: 20px 28px 22px;
    background: rgba(7,11,17,.86); border-left: 5px solid #ffb042; opacity: 0;
    box-shadow: 0 14px 44px rgba(0,0,0,.55); }
  #callout .head { font-size: 56px; letter-spacing: 2px; color: #ffb042; line-height: 1.05; }
  #callout .sub { margin-top: 8px; font-family: 'DejaVu Sans', sans-serif; font-weight: 700;
    font-size: 36px; letter-spacing: 2.5px; color: #dfe8f2; }
  #leader { position: absolute; inset: 0; z-index: 30; }
  #callout { z-index: 41; }
</style>
</head>
<body>
<div id="stage">
  <svg id="mapSvg" width="1920" height="1080" viewBox="0 0 1920 1080">
    <defs>
      <mask id="planMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
        <polyline id="routePlanMask" points="__PLANNED__" fill="none" stroke="#fff" stroke-width="14"/>
      </mask>
    </defs>
    <g id="cam">
      <path class="land" d="__LAND__"/>
      <g id="grat"></g>
      <polyline id="routePlan" points="__PLANNED__" mask="url(#planMask)"/>
      <polyline id="routeAct" points="__ACTUAL__"/>
      <circle class="ring" id="ring1" r="6"/><circle class="ring" id="ring2" r="6"/>
      <circle id="crashCoreSvg" r="7"/>
      <path id="planeMark" d="M0,-11 L8,8 L0,3.4 L-8,8 Z"/>
    </g>
  </svg>
  <svg id="leader" width="1920" height="1080" viewBox="0 0 1920 1080">
    <line id="leaderLine" stroke="#ffb042" stroke-width="2.4" opacity="0"/>
    <circle id="leaderDot" r="4.5" fill="#ffb042" opacity="0"/>
  </svg>
  <div class="ov" id="overlay"></div>
  <div id="callout"><div class="head">60 KM OFF COURSE</div><div class="sub">TURNED NORTH TOO EARLY</div></div>
</div>
<canvas id="grain"></canvas>
<div id="vignette"></div>

<script>window.SCENE = { id: 'sceneD_map', duration: 6.2 };</script>
<script src="../assets/gsap.min.js"></script>
<script src="../assets/core.js"></script>
<script>
// Camera: push 1 -> 2.05 about ORIGIN, easing out over 0..4.2s, then constant.
const ORIGIN = { x: 790, y: 850 };
const CITIES = __CITIES__, REGIONS = __REGIONS__, CRASH = __CRASH__;
const easeIO = (p) => p < .5 ? 2*p*p : 1 - Math.pow(-2*p + 2, 2)/2;
const easeO  = (p) => 1 - Math.pow(1 - p, 3);
const clamp01 = (v) => Math.max(0, Math.min(1, v));
const K = (t) => 1 + 1.05 * easeIO(clamp01(t / 4.2));
const SP = (pt, t) => { const k = K(t); return { x: ORIGIN.x + (pt[0]-ORIGIN.x)*k, y: ORIGIN.y + (pt[1]-ORIGIN.y)*k }; };

// graticule every 10 degrees
(function grat() {
  const g = document.getElementById('grat'); const NS = 'http://www.w3.org/2000/svg';
  const KXv = __KX__, LAT_C = -24, LON_C = -63, S = 30;
  for (let lon = -80; lon <= -40; lon += 10) {
    const x = 960 + (lon - LON_C) * KXv;
    const l = document.createElementNS(NS, 'line');
    l.setAttribute('x1', x); l.setAttribute('x2', x); l.setAttribute('y1', 0); l.setAttribute('y2', 1080);
    l.setAttribute('class', 'grat'); g.appendChild(l);
  }
  for (let lat = -40; lat <= -10; lat += 10) {
    const y = 540 + (LAT_C - lat) * S;
    const l = document.createElementNS(NS, 'line');
    l.setAttribute('x1', 0); l.setAttribute('x2', 1920); l.setAttribute('y1', y); l.setAttribute('y2', y);
    l.setAttribute('class', 'grat'); g.appendChild(l);
  }
})();

// overlay elements
const ov = document.getElementById('overlay');
const cityEls = CITIES.map((c) => {
  const d = document.createElement('div'); d.className = 'city';
  d.innerHTML = `<div class="dot"></div><div class="lab ${c.side}">${c.name}</div>`;
  ov.appendChild(d); return d;
});
const regionEls = REGIONS.map((r) => {
  const d = document.createElement('div');
  d.className = 'region' + (r.name.includes('OCEAN') ? ' ocean' : '');
  d.textContent = r.name; ov.appendChild(d); return d;
});
const cam = document.getElementById('cam');
const plan = document.getElementById('routePlan'), act = document.getElementById('routeAct');
const plane = document.getElementById('planeMark');
const ring1 = document.getElementById('ring1'), ring2 = document.getElementById('ring2');
const core = document.getElementById('crashCoreSvg');
const leaderLine = document.getElementById('leaderLine'), leaderDot = document.getElementById('leaderDot');
const callout = document.getElementById('callout');
const planM = document.getElementById('routePlanMask');
const actLen = act.getTotalLength();
// planned route keeps its dashed pattern; draw-on is done by animating a solid
// twin inside a mask (pathLength dash trick on the mask copy only).
planM.setAttribute('pathLength', '100');
planM.style.strokeDasharray = '100'; planM.style.strokeDashoffset = '100';
act.setAttribute('pathLength', '100');
act.style.strokeDasharray = '100'; act.style.strokeDashoffset = '100';

function drawWin(t, t0, t1) { return easeIO(clamp01((t - t0) / (t1 - t0))); }

window.__onSeek = (t) => {
  const k = K(t);
  cam.setAttribute('transform', `translate(${ORIGIN.x} ${ORIGIN.y}) scale(${k}) translate(${-ORIGIN.x} ${-ORIGIN.y})`);
  // routes
  planM.style.strokeDashoffset = String(100 * (1 - drawWin(t, 2.2, 3.0)));
  const ap = drawWin(t, 2.9, 3.7);
  act.style.strokeDashoffset = String(100 * (1 - ap));
  if (ap > 0 && ap < 1) {
    const pt = act.getPointAtLength(ap * actLen);
    const prev = act.getPointAtLength(Math.max(0, ap * actLen - 2));
    const ang = Math.atan2(pt.y - prev.y, pt.x - prev.x) * 180 / Math.PI + 90;
    plane.setAttribute('transform', `translate(${pt.x} ${pt.y}) rotate(${ang})`);
    plane.style.opacity = '1';
  } else plane.style.opacity = '0';
  // crash marker + pulse rings (SVG space, scales with camera — intended)
  const show = t >= 3.7;
  core.setAttribute('cx', CRASH[0]); core.setAttribute('cy', CRASH[1]);
  core.style.opacity = show ? '1' : '0';
  for (const [ring, off] of [[ring1, 0], [ring2, 0.85]]) {
    if (!show) { ring.style.opacity = '0'; continue; }
    const ph = ((t - 3.7 + off) % 1.7) / 1.7;
    ring.setAttribute('cx', CRASH[0]); ring.setAttribute('cy', CRASH[1]);
    ring.setAttribute('r', String(7 + ph * 34));
    ring.style.opacity = String((1 - ph) * 0.85);
  }
  // overlay: cities
  CITIES.forEach((c, i) => {
    const p = SP(c.xy, t), el = cityEls[i];
    const s = easeO(clamp01((t - c.pop) / 0.18));
    el.style.transform = `translate(${p.x}px,${p.y}px) translate(-50%,-50%) scale(${0.6 + 0.4*s})`;
    el.style.opacity = String(s);
  });
  // regions fade out as the camera pushes in
  const rf = 1 - clamp01((t - 1.6) / 0.9);
  REGIONS.forEach((r, i) => {
    const p = SP(r.xy, t), el = regionEls[i];
    el.style.transform = `translate(${p.x}px,${p.y}px) translate(-50%,-50%)`;
    el.style.opacity = String(rf);
  });
  // callout + leader (the pulsing red marker itself is the crash identifier)
  const cp = SP(CRASH, t);
  const co = clamp01((t - 3.75) / 0.25);
  callout.style.opacity = String(co);
  callout.style.transform = `translateX(${(1 - easeO(co)) * 26}px)`;
  leaderLine.setAttribute('x1', 1036); leaderLine.setAttribute('y1', 946);
  leaderLine.setAttribute('x2', cp.x); leaderLine.setAttribute('y2', cp.y);
  leaderLine.style.opacity = String(co * 0.9);
  leaderDot.setAttribute('cx', cp.x); leaderDot.setAttribute('cy', cp.y);
  leaderDot.style.opacity = String(co);
  window.__grainLevel = 0.07;
};

window.__boot();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    # inject the computed KX into the template's graticule helper
    TEMPLATE = TEMPLATE.replace("__KX__", f"{KX:.3f}")
    main()
