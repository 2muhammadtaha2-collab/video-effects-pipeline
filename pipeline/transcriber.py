# transcription logic here
# first install faster whisper using: pip install faster-whisper   

import json
import os
import subprocess

from faster_whisper import WhisperModel

def extract_audio(video_path, audio_path):
	command = [
		"ffmpeg",
		"-y",
		"-i",
		video_path,
		"-ar",
		"16000",
		"-ac",
		"1",
		"-f",
		"wav",
		audio_path,
	]

	try:
		result = subprocess.run(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			check=True,
		)
	except FileNotFoundError as exc:
		raise RuntimeError("ffmpeg not found") from exc
	except subprocess.CalledProcessError as exc:
		error_text = (exc.stderr or "").strip()
		message = error_text or "ffmpeg failed"
		raise RuntimeError(message) from exc

	return result


def load_model(model_size="base"):
	return WhisperModel(model_size, device="cpu", compute_type="int8")


def transcribe_audio(audio_path, model):
	try:
		segments, info = model.transcribe(audio_path, word_timestamps=True)
	except Exception as exc:
		message = str(exc).strip() or "transcription failed"
		raise RuntimeError(message) from exc

	return segments, info
