# transcription logic here
import json
import os
import shutil
import subprocess

import imageio_ffmpeg
from faster_whisper import WhisperModel


def get_ffmpeg_executable():
	ffmpeg_path = os.getenv("FFMPEG_PATH")
	if ffmpeg_path:
		if os.path.isfile(ffmpeg_path):
			return ffmpeg_path
		else:
			raise RuntimeError(f"FFMPEG_PATH is set but the file does not exist: {ffmpeg_path}")

	system_ffmpeg = shutil.which("ffmpeg")
	if system_ffmpeg:
		return system_ffmpeg

	try:
		return imageio_ffmpeg.get_ffmpeg_exe()
	except Exception as exc:
		raise RuntimeError(
			"ffmpeg not found. Install ffmpeg and add it to PATH, or set FFMPEG_PATH to the ffmpeg executable."
		) from exc


def extract_audio(video_path, audio_path):
	ffmpeg_exe = get_ffmpeg_executable()
	command = [
		ffmpeg_exe,
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
		message = error_text or "unknown ffmpeg error"
		raise RuntimeError(f"ffmpeg failed: {message}") from exc

	return result


def load_model(model_size="base"):
	return WhisperModel(model_size, device="cpu", compute_type="int8")


def transcribe_audio(audio_path, model):
	try:
		segments, info = model.transcribe(audio_path, word_timestamps=True)
	except Exception as exc:
		message = str(exc).strip() or "unknown transcription error"
		raise RuntimeError(f"transcription failed: {message}") from exc

	return segments, info


def build_transcript(segments, language):
	words = []
	for segment in segments:
		for word in segment.words:
			clean_word = word.word.strip()
			words.append(
				{
					"word": clean_word,
					"start": round(word.start, 2),
					"end": round(word.end, 2),
				}
			)

	sentences = []
	chunk = []
	for word in words:
		chunk.append(word)
		if word["word"].endswith((".", "!", "?")) or len(chunk) >= 6:
			sentences.append(
				{
					"text": " ".join(w["word"] for w in chunk),
					"start": chunk[0]["start"],
					"end": chunk[-1]["end"],
				}
			)
			chunk = []

	if chunk:
		sentences.append(
			{
				"text": " ".join(w["word"] for w in chunk),
				"start": chunk[0]["start"],
				"end": chunk[-1]["end"],
			}
		)

	return {"language": language, "words": words, "sentences": sentences}


def save_transcript(data, output_path):
	try:
		with open(output_path, "w", encoding="utf-8") as file:
			json.dump(data, file, indent=4, ensure_ascii=False)
	except Exception as exc:
		message = str(exc).strip() or "unknown save error"
		raise RuntimeError(f"save failed: {message}") from exc


def get_autoshorts_root():
	return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def transcribe_video(video_path, transcript_path, model_size="base"):
	if not os.path.isfile(video_path):
		raise FileNotFoundError(video_path)

	base_dir = get_autoshorts_root()
	temp_dir = os.path.join(base_dir, "temp")
	os.makedirs(temp_dir, exist_ok=True)

	audio_path = os.path.join(temp_dir, "audio.wav")
	if not os.path.isabs(transcript_path):
		transcript_path = os.path.join(base_dir, transcript_path)
	print("extracting audio...")
	extract_audio(video_path, audio_path)
	print("loading model...")
	model = load_model(model_size)
	print("transcribing...")
	segments, info = transcribe_audio(audio_path, model)
	transcript = build_transcript(segments, info.language)
	print("saving transcript...")
	save_transcript(transcript, transcript_path)
	print("done")
	return transcript


if __name__ == "__main__":
	base_dir = get_autoshorts_root()
	# video_path = os.path.join(base_dir, "uploads", "test_clip.mp4")
	video_path = os.path.join(base_dir, "test_clip.mp4")
	transcript = transcribe_video(video_path, "transcript.json", "tiny")
	print(len(transcript["words"]))
