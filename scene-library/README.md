# Scene Library — reusable components

Every scene type built for a video is stored here so the next video reuses it instead of starting over. Capture tool: `capture.mjs` (deterministic headless-Chrome frame capture, adapted from the faceless-shorts pattern).

| Component | Source | Notes |
|---|---|---|
| `radio-dial/` | Andes proof v1, scene 1 | Vintage radio dial, needle hunt + lock, kinetic headline slams, PRESUMED DEAD stamp. Strong component — keep. |
| `ridge-stylised/` | Andes proof v1, scene 2 | Flat-design layered ridges + parallax + snowfall. FLAGGED in LESSONS #12: stylised only; a photo-based ridge treatment is preferred for hero shots. |
| `map-stylised/` | Andes proof v1, scene 3 | Hand-drawn outline map. RETIRED 2026-11-16 — replaced by `map-natural-earth/` (proof v2). Do not use. |
| `map-natural-earth/` | Andes proof v2, scene 4 | Real-data route map: Natural Earth coastline (public domain), generator `gen_map.py`, planned vs actual routes, crash marker + pulse, callout. See its README for reuse + label-collision rules. |
| `photo-treatment/` | Andes proof v2, scenes 1 & 3 | Real-photo treatment: cold grade, push-in/drift, two-layer snowfall, typed lower-third. Generator `make_photo_scene.py`. Photo at full opacity from frame 0 (no fade-from-black). Preferred for hero shots. |
| `radio-dial/` (v2) | Andes proof v2, scene 2 | v1 component rebuilt LARGE (dial 1380px ≈ 72% of frame width), headline slams synced to spoken words 7.52–9.83, stamp at 12.57. Source scene: prod2/v2/scenes/sceneB_radio.html. |

New components are added with: the HTML source, a one-line description, and any usage notes (timing config, known limits).
