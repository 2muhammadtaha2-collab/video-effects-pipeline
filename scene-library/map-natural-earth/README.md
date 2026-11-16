# map-natural-earth — real-data route map component

Built for Andes proof v2 (2026-11-16), replacing the retired hand-drawn `map-stylised/` (LESSONS #12: maps must use real geographic data).

**Generator:** `gen_map.py` — takes Natural Earth coastline data + a config of cities/routes and emits a self-contained scene HTML (1920×1080) that runs on the shared core engine (`core.js` snowfall/grain + GSAP), captured with the standard `capture.mjs`.

**Data:** `data/ne_50m_land.geojson` — Natural Earth 1:50m land polygons, **public domain**, via the nvkelso/natural-earth-vector GitHub mirror. Do not substitute hand-drawn outlines.

**How it works:**
- Equirectangular projection (`--clon/--clat` centre, `--scale` px per degree of latitude).
- Cities are placed from real lon/lat. Planned route = dashed line drawn on with an SVG-mask reveal (dash pattern preserved — a plain dashoffset draw makes the line solid). Actual route = amber line with a plane marker riding it via `offset-path`.
- Crash/event marker with expanding pulse rings; callout box with leader line.
- Camera push: closed-form scale on the world group toward a focal point.

**Andes v2 config (example scene: `example_sceneD_map.html`):** centre (−63, −24), scale 30; planned Montevideo → Mendoza → Malargüe → Curicó → Santiago (dashed), actual Montevideo → Mendoza → Malargüe → turn point (−70.53, −34.98) → crash (−70.286, −34.765); callout "60 KM OFF COURSE / TURNED NORTH TOO EARLY" fully in by global 20.5s.

**Usage notes / known limits:**
- Reuse for a new story: edit CITIES / routes / beats in `gen_map.py` (times are local to the scene; convert to global when writing the shot list).
- Keep all labels ≥34px at 1080p (Bible). Check label collisions at the FINAL camera position with a probe frame before rendering — dense city clusters (Curicó/Malargüe/Santiago) collide easily; drop or offset tags, never shrink type.
- Keep the callout clear of the caption band (bottom ~120px) or shift late captions with ASS margins (proof v2 used MarginR 760 for events ≥19.0s).
- Ocean labels must sit on water at the final zoom, not at the wide view.
