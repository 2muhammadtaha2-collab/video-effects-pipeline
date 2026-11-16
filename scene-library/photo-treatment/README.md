# photo-treatment — real photograph scene component

Built for Andes proof v2 (2026-11-16). Takes a real photograph (archival / Wikimedia Commons, licence checked per file) and produces a full-frame scene: cold grade, slow push-in/drift, two-layer snowfall, film grain, optional typed lower-third. This is the preferred treatment for hero shots (LESSONS #12: mix animation with real photos; stylised scenes flagged).

**Generator:** `make_photo_scene.py` — emits a scene HTML (1920×1080) on the shared core engine, captured with the standard `capture.mjs`. Motion is a closed-form function of t (deterministic capture).

**Key parameters:** `--imgw/--left/--top` (photo placement), `--scale0/--scale1` (push-in), `--dx/--dy` (drift), `--origin` (push focal point), `--title/--subtitle` (lower-third), `--ltbottom` (raise the lower-third to clear the burned-in caption band — proof v2 used 196).

**Hard rules baked in after v2 QC:**
- The photo is at **full opacity from frame 0** — hard cut in, never a fade from black. (v2's first render had black frames at 0.0s and at the 13.0s cut; both failed frame QC.)
- The typewriter caret is hidden until typing actually starts.
- Lower-third type: title 60px, subtitle 34px (phone-large, Bible minimums); typing completes early enough that the full line holds ≥2s.

**Licences:** every photo's own file licence is checked individually and logged in the production's ASSETS.md with its credit line (CC0/CC BY family only, never NC — LESSONS #18). Proof v2 examples: `example_sceneA_flash.html` (crash-site photo, public domain) and `example_sceneC_photo.html` (wreckage photo, CC BY-SA 4.0) — photo files themselves live in the production's assets folder, not the library.
