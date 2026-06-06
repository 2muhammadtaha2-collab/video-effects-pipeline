from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import cv2
import os
import json


def apply_zoom_effect(clip, zoom_factor=1.3):
    """Gradually zooms into the video over its duration."""
    duration = clip.duration

    def zoom(get_frame, t):
        scale = 1 + (zoom_factor - 1) * (t / duration)
        frame = get_frame(t)
        h, w = frame.shape[:2]
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(frame, (new_w, new_h))
        x = (new_w - w) // 2
        y = (new_h - h) // 2
        return resized[y:y+h, x:x+w]

    return clip.transform(zoom)


def apply_effects(rendered_clips, transcript):
    output = []

    for clip_info in rendered_clips:
        clip_id = clip_info["clip_id"]
        clip_path = clip_info["path"]

        # FIX 4: Get the clip's start time in the original video
        # Sohaib's renderer should include this in clip_info
        clip_start = clip_info.get("start_time", 0)

        print(f"Processing clip {clip_id} (original start: {clip_start}s)...")

        clip = VideoFileClip(clip_path)
        zoomed_clip = apply_zoom_effect(clip, zoom_factor=1.3)

        all_clips = [zoomed_clip]

        # --- Captions (white sentence-level text at bottom) ---
        for sentence in transcript["sentences"]:

            # FIX 4: Convert global timestamps to clip-local timestamps
            local_start = sentence["start"] - clip_start
            local_end = sentence["end"] - clip_start

            # Skip if sentence is completely outside this clip
            if local_start >= clip.duration or local_end <= 0:
                continue

            # Clamp to clip boundaries
            local_start = max(0, local_start)
            local_end = min(local_end, clip.duration)

            txt = (
                TextClip(
                    font="C:/Windows/Fonts/arial.ttf",
                    text=sentence["text"],
                    font_size=40,
                    color="white",
                    stroke_color="black",
                    stroke_width=2,
                    size=(zoomed_clip.w - 40, None),  # FIX 2: use zoomed_clip.w
                    method="caption"
                )
                .with_start(local_start)
                .with_duration(local_end - local_start)
                .with_position(("center", int(zoomed_clip.h * 0.82)))
            )
            all_clips.append(txt)

        # --- Word Highlights (yellow per-word text in center) ---
        for word_info in transcript.get("words", []):

            # FIX 4: Convert global timestamps to clip-local timestamps
            local_start = word_info["start"] - clip_start
            local_end = word_info["end"] - clip_start

            # Skip if word is completely outside this clip
            if local_start >= clip.duration or local_end <= 0:
                continue

            # Clamp to clip boundaries
            local_start = max(0, local_start)
            local_end = min(local_end, clip.duration)

            # FIX 1: Use a lambda for relative vertical positioning (65% down)
            # Passing ("center", 0.65) does NOT work in moviepy — it ignores
            # or misinterprets the float. Use a lambda with pixel calculation.
            clip_height = zoomed_clip.h
            txt = (
                TextClip(
                    font="C:/Windows/Fonts/arial.ttf",
                    text=word_info["word"],
                    font_size=70,
                    color="yellow",
                    stroke_color="black",
                    stroke_width=3,
                )
                .with_start(local_start)
                .with_duration(local_end - local_start)
                .with_position((0.5, 0.65), relative=True) # FIX 1
            )
            all_clips.append(txt)

        final_clip = CompositeVideoClip(all_clips)

        os.makedirs("shorts_output", exist_ok=True)
        output_path = f"shorts_output/final_clip_{clip_id}.mp4"
        final_clip.write_videofile(output_path, codec="libx264")

        # FIX 3: Close all clips to prevent memory leaks and Windows file locks
        final_clip.close()
        zoomed_clip.close()
        clip.close()

        output.append({
            "clip_id": clip_id,
            "path": output_path,
            "captions": True,
            "zoom": True
        })

    return output


# ---- TEST WITH REAL TRANSCRIPT ----
if __name__ == "__main__":

    with open("transcript.json", "r") as f:
        real_transcript = json.load(f)

    # Build sentences from words
    words = real_transcript["words"]
    sentences = []
    chunk = []

    for word in words:
        chunk.append(word)
        if word["word"].endswith((".", "!", "?")) or len(chunk) >= 6:
            sentences.append({
                "text": " ".join(w["word"] for w in chunk),
                "start": chunk[0]["start"],
                "end": chunk[-1]["end"]
            })
            chunk = []

    if chunk:
        sentences.append({
            "text": " ".join(w["word"] for w in chunk),
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"]
        })

    real_transcript["sentences"] = sentences

    # start_time = 0 means transcript timestamps already match the test clip
    dummy_clips = [
        {"clip_id": 1, "path": "test_clip.mp4", "start_time": 0}
    ]

    result = apply_effects(dummy_clips, real_transcript)
    print(result)