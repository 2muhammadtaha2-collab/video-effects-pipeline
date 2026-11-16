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
- **ASSETS.md per video**: every photo, sound and music file, with source, licence and credit line. Music and sounds: **CC0 or CC BY only, never NC**. Photos: each file's own licence checked individually.

## 8. Topic research (browser only — vidIQ is not used for research)
- YouTube: search the niche, filter by view count and by upload date. Open the top channels' "Popular" tab. Look for outliers: videos with far more views than the channel's subscriber count or its usual videos.
- YouTube search suggestions: type the topic and record what autocomplete offers. That is what people actually search.
- Google Trends and Wikipedia pageview stats: check the story has steady or rising interest in US, UK and Canada.
- Reddit history and mystery communities: see which stories get the most discussion and which questions people keep asking.
- Output to Taha: 3 topics, each with the one-sentence story, the best existing video on it (views, age, channel size), and the angle nobody has used yet. He picks.

## 9. Hook and script research
- For the chosen topic, read the transcripts of the 5 best performing videos. Note how each opens in the first 30 seconds, where the reveals fall, and what the top comments say viewers loved or found missing.
- Use this only to learn structure. Never copy sentences, scene order or titles. Every script is written fresh from our own dossier.

## 10. Script and story standard
- Topic test: the story fits in one sentence with an impossible choice or a contradiction in it.
- Title and thumbnail first: 3 plain curiosity titles under 60 characters and one thumbnail idea, approved by Taha before any script is written.
- Hook: open inside the most dramatic moment, never with background or a channel intro. By 30 seconds the viewer knows the stakes and the question the ending will answer.
- Open loops: one unanswered question is always running. Close one, open the next. A reveal, reversal or new danger every 45 to 60 seconds.
- People: follow one main character. Use real names, ages, exact words and small physical details from the dossier.
- Ending: deliver what the title promised, land the last line, no long outro.
- Language: short sentences written for the ear, about 150 words a minute. Cut any paragraph the story survives without.
- Truth: nothing invented, disputed points labelled, no title the video does not pay off.
- Every script comes with a retention map: a table of timestamps showing which hook or open question is active.

## 11. Research limits
- At most 10 videos studied per topic, one research pass per video.
- Save all research to RESEARCH.md in the repo so it is never repeated.
- Report findings as numbers and links, not opinions.
