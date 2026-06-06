# autoshorts

AI video shorts generator

## Setup

- First install faster-whisper using: pip install faster-whisper
- Then install ffmpeg from https://www.gyan.dev/ffmpeg/builds/
- Install ffmpeg-release-essentials.zip and add the bin folder path to your PATH environment variable
- Then run python pipeline/transcriber.py
# 🎬 Video Effects Pipeline

A Python module that automatically adds **zoom effects**, **captions**, and **word-by-word highlighting** to videos — replicating the viral short-form video style seen on TikTok, YouTube Shorts, and Instagram Reels.

Built as part of the **AutoShorts AI** internship project — an end-to-end pipeline that converts long-form videos into engaging short clips automatically.

---

## ✨ Features

- 🔍 **Zoom Effect** — Smooth punch-in zoom that gradually scales the video over its duration
- 💬 **Auto Captions** — White sentence-level captions synced to transcript timestamps
- ⚡ **Word Highlighting** — Each word lights up in yellow as it is spoken, TikTok style

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.14 | Core language |
| MoviePy 2.x | Video editing and effects |
| OpenCV | Frame-level zoom processing |
| ffmpeg | Video encoding and audio handling |
| Pillow | Text rendering |
| NumPy | Frame manipulation |

---

## 📁 Project Structure

```
video-effects-pipeline/
│
├── pipeline/
│   └── effects.py        ← Main module
│
├── shorts_output/        ← Processed videos saved here
├── transcript.json       ← Word-level transcript input
├── requirements.txt      ← Python dependencies
└── README.md
```

---

## ⚙️ How It Works

The module exposes a single function:

```python
apply_effects(rendered_clips, transcript) -> list
```

### Input
```python
rendered_clips = [
    {"clip_id": 1, "path": "shorts_output/clip_1.mp4", "start_time": 0}
]

transcript = {
    "words": [
        {"word": "Hello", "start": 0.52, "end": 0.83},
        {"word": "everyone", "start": 0.84, "end": 1.30}
    ],
    "sentences": [
        {"text": "Hello everyone welcome back.", "start": 0.52, "end": 3.45}
    ]
}
```

### Output
```python
[
    {
        "clip_id": 1,
        "path": "shorts_output/final_clip_1.mp4",
        "captions": True,
        "zoom": True
    }
]
```

---

## 🚀 Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/2muhammadtaha2-collab/video-effects-pipeline.git
cd video-effects-pipeline
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install moviepy opencv-python ffmpeg-python pillow numpy
```

### 4. Install ffmpeg (Windows)
- Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
- Extract and add `bin` folder to system PATH

### 5. Run the module
```bash
python pipeline/effects.py
```
```
Transcribe → Score → Select Clips → Render → Effects ← (this module)
```

| Step | Module | Owner |
|---|---|---|
| 1 | Transcriber | Hamza Azam |
| 2 | Scorer | Ali Zain |
| 3 | Clip Selector | Muhammad Hamza |
| 4 | Renderer | Sohaib |
| 5 ★ | **Effects & Captions** | **Muhammad Taha** |

---

## 👨‍💻 Author

**Muhammad Taha**
- GitHub: [@2muhammadtaha2-collab](https://github.com/2muhammadtaha2-collab)
- Built during AI Video Pipeline Internship — June 2026
