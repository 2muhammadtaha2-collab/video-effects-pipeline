// Deterministic frame capture for prod2 scenes (HyperFrames pattern, adapted
// from the faceless-shorts skill's tools/capture.mjs to 1920x1080 DOM scenes).
// Animations are never played: for each frame we seek the scene's GSAP timeline
// to t = frame/fps via window.__seekAndRender(t), wait for the compositor to
// present, then grab the surface with Page.captureScreenshot and pipe JPEG
// frames into ffmpeg (libx264, yuv420p). Same input -> same frames.
//
// Environment notes (this VM's Chromium build):
//  - It refuses to start without --hatch-webgl-allowed-domains-file + its sha256.
//  - It blocks http://127.0.0.1 pages (ERR_BLOCKED_BY_LOCAL_NETWORK_ACCESS_CHECKS),
//    so scenes are loaded via file:// URLs passed as the launch argument and the
//    page target is found through /json/list. --allow-file-access-from-files lets
//    the pages load their fonts/scripts across directories.
//
//   node tools/capture.mjs                 render every scene in scenes.json
//   node tools/capture.mjs scene1_radio    render one scene
//   node tools/capture.mjs probe scene1_radio 1.0,5.4,9.0   stills to frames_tmp/
// CHROME=/path/to/chrome overrides the browser (default /opt/meta-chromium/chrome).
import { spawn } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CFG = JSON.parse(fs.readFileSync(path.join(ROOT, 'scenes.json'), 'utf8'));
const FPS = CFG.fps, W = CFG.width, H = CFG.height;
const CHROME = process.env.CHROME || '/opt/meta-chromium/chrome';
const POLICY = '/var/lib/hatch-browser/rootfs-base/usr/share/hatch/chromium/webgl-allowed-domains.txt';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const [mode, arg2, arg3] = process.argv.slice(2);

async function openScene(file) {
  const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'prod2-chrome-'));
  const policySha = crypto.createHash('sha256').update(fs.readFileSync(POLICY)).digest('hex');
  const url = 'file://' + path.join(ROOT, file);
  const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${prof}`,
    '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', `--window-size=${W},${H}`,
    '--force-device-scale-factor=1', '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
    '--allow-file-access-from-files',
    `--hatch-webgl-allowed-domains-file=${POLICY}`, `--hatch-webgl-allowed-domains-sha256=${policySha}`,
    ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []), url], { stdio: 'ignore' });
  let dbg;
  for (let i = 0; i < 200 && !dbg; i++) { try { dbg = fs.readFileSync(path.join(prof, 'DevToolsActivePort'), 'utf8').split('\n')[0].trim(); } catch { await sleep(100); } }
  if (!dbg) throw new Error('Chrome did not start');
  let target;
  for (let i = 0; i < 100 && !target; i++) {
    try { const list = await (await fetch(`http://127.0.0.1:${dbg}/json/list`)).json(); target = list.find((t) => t.type === 'page' && t.url === url); } catch {}
    if (!target) await sleep(150);
  }
  if (!target) throw new Error('page target not found for ' + url);
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let id = 0; const pend = new Map(); const logs = [];
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) { const p = pend.get(m.id); pend.delete(m.id); m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); }
    else if (m.method === 'Runtime.exceptionThrown') logs.push('EXCEPTION ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
    else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') logs.push('ERROR ' + m.params.args.map((a) => a.value ?? a.description).join(' '));
  };
  const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expr) => { const x = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); if (x.exceptionDetails) throw new Error(x.exceptionDetails.exception?.description || x.exceptionDetails.text); return x.result.value; };
  await send('Runtime.enable'); await send('Page.enable');
  // This build's headless window reserves ~137px for browser UI (1920x1080 window
  // -> 1920x943 viewport). Force the exact composition size via emulation.
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  for (let i = 0; ; i++) {
    const st = await ev('window.__ready === true').catch(() => false);
    if (st) break;
    if (i > 300) throw new Error('page boot timeout\n' + logs.join('\n'));
    await sleep(100);
  }
  if (logs.length) console.log('page logs:', logs.join(' | '));
  const shot = async (t, format = 'png', quality = undefined) => {
    await ev(`window.__seekAndRender(${t})`);
    const s = await send('Page.captureScreenshot', { format, quality, fromSurface: true, captureBeyondViewport: false });
    return Buffer.from(s.data, 'base64');
  };
  const close = () => { try { ws.close(); } catch {} chrome.kill('SIGKILL'); setTimeout(() => { try { fs.rmSync(prof, { recursive: true, force: true }); } catch {} }, 300); };
  return { ev, shot, close };
}

if (mode === 'probe') {
  const sc = CFG.scenes.find((s) => s.id === arg2);
  if (!sc) throw new Error('unknown scene ' + arg2);
  const P = await openScene(sc.file);
  fs.mkdirSync(path.join(ROOT, 'frames_tmp'), { recursive: true });
  for (const t of (arg3 || '0').split(',').map(Number)) {
    fs.writeFileSync(path.join(ROOT, 'frames_tmp', `${sc.id}_t${t.toFixed(1)}.jpg`), await P.shot(t, 'jpeg', 90));
    console.log(`probe ${sc.id} @ ${t}s`);
  }
  P.close();
} else {
  const scenes = CFG.scenes.filter((s) => !mode || s.id === mode);
  if (!scenes.length) throw new Error('no scene matched ' + mode);
  for (const sc of scenes) {
    const out = path.join(ROOT, sc.out); fs.mkdirSync(path.dirname(out), { recursive: true });
    const P = await openScene(sc.file);
    const n = Math.round(sc.duration * FPS);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      // JPEG frames arrive full-range (yuvj); convert to limited-range yuv420p
      '-vf', 'scale=in_range=pc:out_range=tv', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      // JPEG q92, not PNG: grain-heavy frames make PNG capture/pipe several
      // times slower, and the final encode is lossy anyway (same choice as
      // the faceless-shorts capture tool).
      const b = await P.shot(i / FPS, 'jpeg', 92);
      if (!ff.stdin.write(b)) await new Promise((r) => ff.stdin.once('drain', r));
      if (i % 48 === 0) process.stdout.write(`\r${sc.id}: ${i}/${n} frames`);
    }
    ff.stdin.end(); await new Promise((r) => ff.on('close', r));
    P.close();
    console.log(`\r${out} — ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
}
