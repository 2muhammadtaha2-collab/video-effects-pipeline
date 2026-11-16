# LESSONS — permanent rules from Taha's feedback

*Every entry came from Taha's actual feedback. Never repeat a mistake listed here. New feedback is added the same day it is given.*

## From the Andes v1 rejection (16 Nov 2026)
1. Still images with a slow zoom are a slideshow, not animation. Never deliver them as video, and never call them cinematic.
2. A free local TTS voice (Kokoro) that sounds robotic fails the voice bar. Voice is locked to Ryan; do not substitute silently.
3. A synthesised low drone is not sound design and not music.
4. Copying a reference channel's format (e.g. text-only, no voiceover) never overrides Taha's own standing instructions. Where they conflict, flag it and ask — or follow Taha's rule.
5. Never oversell a delivery. If the method can't support the adjective, don't use the adjective.

## From the animated proof v1 review (16 Nov 2026)
6. The first seconds are the hook window: a small element in one part of the frame with the rest static fails, even if one needle moves. The opening's strongest visual goes in the first 5 seconds, full-frame.
7. Sound effects must exist on every key visual event and must be audible on a phone speaker — check for mid/high content, not only bass.
8. Captions must never stack or glitch position (seen at ~5.7s and ~20.1s in proof v1 — caused by overlapping caption events; clamp event timings so events can never overlap).
9. Captions hide while a headline card shows the same words (proof v1 duplicated the headline for ~5 seconds).
10. A label that is still fading in when the clip ends is a fail. Every readable element completes its entrance and holds at least 2 seconds.
11. Check every on-screen claim against the dossier — proof v1's map said "turned west too early"; the dossier says the crew turned **north** too early and descended while still 60–69 km east of Curicó.
12. Hand-drawn map outlines and flat-triangle mountains read as basic art. Maps use real geographic data; mix in real photos so a long video in one dark palette doesn't feel flat.
13. Small mono labels are unreadable on phones. Text meant to be read is phone-large.

## From Taha's production-standard follow-up (16 Nov 2026)
16. Production files (PRODUCTION_BIBLE.md, LESSONS.md, scene-library/, ASSETS.md) are committed to the GitHub repo (video-effects-pipeline) — the repo is their permanent home, not just this machine.
17. Proof and video deliveries attach the evidence, not just verdicts: the half-second frame sheets and the measured numbers (loudness, effect timings, transcript diff) come with the QC report.
18. Music and sound licences: CC0 or CC BY only — never NC (non-commercial). Photos: check each file's own licence individually. ASSETS.md logs source, licence AND credit line for every asset.
19. Azure is not available yet — keep the current voice route (Ryan via free web front-ends) and never block production waiting on it. Taha creates the YouTube channel himself and downloads Audio Library tracks that Muse names.
20. Every video description carries the CC BY credit line for every track used (music and sound), copied from ASSETS.md. No description ships without its credits block.
21. Outside skills (cinetic, video-shotcraft) are built for films under 90 seconds; ours is a 10-minute narrated documentary. Narration leads: cuts and text land on Ryan's words, music sits underneath. Never cut to the music beat. (Approved 16 Nov 2026; adoption happens only after the proof passes.)
22. Adopt cinetic's measurable rules into PRODUCTION_BIBLE.md — motion carried across every cut, sound within 30 ms of each cut, no snapping or frozen motion. After the proof passes, not before.
23. Only 10–15 devices suited to dark history get picked from the skills, listed for Taha's approval before any are built. No product-ad style moves.
24. QC must measure the on-screen duration of every text element and print in/out times in the QC report. Any element meant to be read — stamps, lower-thirds, callouts — must measure at least 2 s fully visible. (Proof v2's PRESUMED DEAD stamp was prominent for only ~0.4 s and QC still passed it. Never again.)
25. A "shot" is what the viewer sees, not what freezedetect reports. QC judges visible change from the frames; a technically changing but visually static scene counts as static.
26. No single element (for example the radio dial) is the only thing on screen for more than 4 s. Long beats get cutaways to real material and the frame stays filled.
27. Maps zoom to the region where the action happens so the key movement fills the frame. Labels never touch or overlap. Something moves from the first second of the scene.
28. Music ducking releases when the voice pauses — the music comes up in the gaps — and the bed must be audible above 200 Hz, not only bass.
29. A date on screen must say what it is: label it with its event (for example "CRASHED — 13 OCTOBER 1972"), never a bare date the viewer has to interpret.
30. Build in segments: after the proof passes, build the first 90 seconds only and stop for Taha's approval before building more. Never build a full video in one pass again.
31. Carry-over fix for the Andes build (from proof v3 approval, 16 Nov 2026): the music must stay audible in the pause after "called off" — that silence is a story beat, and the bed carries it; never let the mix drop to near-silence there.
32. Carry-over fix for the Andes build: the 4.4 s cutaway photo shows a modern-day visitor at the wreckage. In the build, crop him out or label the shot as the site today — a modern person must never sit unlabelled inside a 1972 scene.

## Standing process lessons
14. Quality over completion, always — Taha's overnight brief said it, the Andes v1 delivery violated it. If finishing and quality conflict, quality wins and Taha hears about it before delivery.
15. Verify before claiming: files, durations, loudness, caption sync and voice completeness are measured, not assumed.
