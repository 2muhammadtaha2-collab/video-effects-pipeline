# PRODUCTION BIBLE — Dark History & Survival Channel

*Standing standard for every video. Read before every production. Set by Taha, 16 Nov 2026. The goal is never "a finished video" — it is a video a viewer would not click away from.*

## Locked decisions
- **Voice: Ryan** (Microsoft neural en-GB-RyanNeural). No other narrator.
- **Budget: zero.** No paid tools, subscriptions, or assets until the channel earns.
- **No deadline.** Never trade quality for speed. If the bar cannot be met, stop and say exactly what is needed (see No Silent Trade-Offs).
- **Never describe work with quality adjectives** ("cinematic", "professional", "publication-ready") that the production method does not support. Report measured facts.

## 1. Visual bar
- The first 5 seconds contain the strongest visual of the opening.
- No shot stays unchanged for more than 4 seconds. Use the full frame — no small centred elements floating in empty space.
- Mix animation with real archival photos, documents and newspapers. Animation alone reads as an infographic.
- Maps use real geographic data (e.g. Natural Earth), never hand-drawn outlines.
- Anything meant to be read is large enough for a phone and stays on screen at least 2 seconds.
- Vary palette and scene type by chapter. Never two scenes of the same type back to back.

## 2. Sound bar
- Four layers in every video: **voice, music, ambience, and a sound effect on every key visual event** (text landing, map point, cut, stamp, reveal).
- Sound must be audible on phone speakers — include mid/high frequency content; low bass alone (e.g. a 55 Hz drone at -33 dB) does not count as sound design.
- Target about **-14 LUFS**, peaks under **-1 dB** true peak. Music ducked under the voice.

## 3. Story and facts bar
- Every on-screen fact, number and label is checked against the video's fact dossier before rendering.
- Captions never overlap each other, never stack, never sit in the wrong position.
- Captions hide while a headline card shows the same words.

## 4. Process — stop at each gate for Taha's approval
**Topic → fact dossier → script → narration → shot list → ~25s proof → full build → QC → delivery.**

- The shot list is a table: time · narration line · what moves · what sound plays.
- If a script, hook, title or scene ideas would be better from Claude, write Taha a complete ready-to-paste request for Claude and wait for what he brings back.
- Each gate message is short: what to look at, and what is needed from him.

## 5. QC — check your own work before showing it
A video cannot be judged by describing it. After every render:
- Extract a frame every 0.5 seconds and look at each one.
- Run freeze detection (ffmpeg freezedetect); find any caption overlap or text cut off early.
- Measure loudness; confirm each planned sound effect is actually present in the audio.
- Transcribe the narration back and compare it word-by-word with the script.
- Send a QC report: pass or fail per rule in sections 1–3, with measured facts. List every failure. No quality adjectives. **If anything fails, fix it before Taha sees it.**

## 6. No silent trade-offs
If the bar cannot be reached because of budget, machine limits, a blocked network or a missing tool — stop and tell Taha exactly what is needed (a connection, a free signup, a file). He will set it up. Downgrading quietly and delivering anyway is the one unforgivable failure.

## 7. Permanent infrastructure
- **LESSONS.md** (same folder): every piece of feedback from Taha becomes a permanent rule there, the same day. Never repeat a mistake already listed.
- **scene-library/**: every scene type built becomes a reusable component, stored here with its source.
- **ASSETS.md per video**: every photo, sound and music file, with source and licence.
