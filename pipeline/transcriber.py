# transcription logic here
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

	return {"language": language, "words": words}


def save_transcript(data, output_path):
	try:
		with open(output_path, "w", encoding="utf-8") as file:
			json.dump(data, file, indent=4, ensure_ascii=False)
	except Exception as exc:
		message = str(exc).strip() or "unknown save error"
		raise RuntimeError(f"save failed: {message}") from exc


def transcribe_video(video_path, transcript_path, model_size="base"):
	if not os.path.isfile(video_path):
		raise FileNotFoundError(video_path)

	temp_dir = "temp"
	if not os.path.isdir(temp_dir):
		os.makedirs(temp_dir)

	audio_path = "temp/audio.wav"
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
	transcript = transcribe_video("autoshorts/uploads/test.mp4", "transcript.json", "tiny")
	print(len(transcript["words"]))
