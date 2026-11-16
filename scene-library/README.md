# Scene Library — reusable components

Every scene type built for a video is stored here so the next video reuses it instead of starting over. Capture tool: `capture.mjs` (deterministic headless-Chrome frame capture, adapted from the faceless-shorts pattern).

| Component | Source | Notes |
|---|---|---|
| `radio-dial/` | Andes proof v1, scene 1 | Vintage radio dial, needle hunt + lock, kinetic headline slams, PRESUMED DEAD stamp. Strong component — keep. |
| `ridge-stylised/` | Andes proof v1, scene 2 | Flat-design layered ridges + parallax + snowfall. FLAGGED in LESSONS #12: stylised only; a photo-based ridge treatment is preferred for hero shots. |
| `map-stylised/` | Andes proof v1, scene 3 | Hand-drawn outline map. FLAGGED in LESSONS #12: replace with Natural Earth real-data map (`map-natural-earth/`) and retire this one. |

New components are added with: the HTML source, a one-line description, and any usage notes (timing config, known limits).
