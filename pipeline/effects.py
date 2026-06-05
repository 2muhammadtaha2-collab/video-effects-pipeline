from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import cv2
import os


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


def add_captions(clip, transcript):
    """Adds basic white captions at the bottom of the video."""
    clips = [clip]

    for sentence in transcript["sentences"]:
        text = sentence["text"]
        start = sentence["start"]
        end = sentence["end"]
        duration = end - start

        if start >= clip.duration:
            continue

        txt_clip = (
            TextClip(
                font="C:/Windows/Fonts/arial.ttf",
                text=text,
                font_size=40,
                color="white",
                stroke_color="black",
                stroke_width=2,
                size=(clip.w - 40, None),
                method="caption"
            )
            .with_start(start)
            .with_duration(duration)
            .with_position(("center", "bottom"))
        )

        clips.append(txt_clip)

    return CompositeVideoClip(clips)


def apply_effects(rendered_clips, transcript):
    output = []

    for clip_info in rendered_clips:
        clip_id = clip_info["clip_id"]
        clip_path = clip_info["path"]

        print(f"Processing clip {clip_id}...")

        clip = VideoFileClip(clip_path)
        zoomed_clip = apply_zoom_effect(clip, zoom_factor=1.3)
        final_clip = add_captions(zoomed_clip, transcript)

        os.makedirs("shorts_output", exist_ok=True)
        output_path = f"shorts_output/final_clip_{clip_id}.mp4"
        final_clip.write_videofile(output_path, codec="libx264")

        output.append({
            "clip_id": clip_id,
            "path": output_path,
            "captions": True,
            "zoom": True
        })

        clip.close()

    return output


# ---- TEST WITH DUMMY DATA ----
if __name__ == "__main__":
    dummy_clips = [
        {"clip_id": 1, "path": "test_clip.mp4"}
    ]

    dummy_transcript = {
        "words": [
            {"word": "Hello", "start": 0.52, "end": 0.83},
            {"word": "everyone", "start": 0.84, "end": 1.30}
        ],
        "sentences": [
            {"text": "Hello everyone welcome back.", "start": 0.52, "end": 3.45}
        ]
    }

    result = apply_effects(dummy_clips, dummy_transcript)
    print(result)

# ---- TEST WITH REAL TRANSCRIPT ----
if __name__ == "__main__":
    import json

    with open("transcript.json", "r") as f:
        real_transcript = json.load(f)

    # Build sentences from words since transcript.json has no sentences
    words = real_transcript["words"]
    sentences = []
    chunk = []

    for word in words:
        chunk.append(word)
        if word["word"].endswith((".","!","?")) or len(chunk) >= 6:
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

    dummy_clips = [
        {"clip_id": 1, "path": "test_clip.mp4"}
    ]

    result = apply_effects(dummy_clips, real_transcript)
    print(result)