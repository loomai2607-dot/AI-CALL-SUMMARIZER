import os
import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    print(f"🎧 Starting transcription for: {audio_path}")

    if not os.path.exists(audio_path):
        print(f"❌ File does not exist: {audio_path}")
        return None

    try:
        result = model.transcribe(audio_path)
        transcript = result.get("text", "").strip()

        if not transcript:
            print("❌ Transcription returned empty text.")
            return None

        print(f"✅ Transcription successful. Sample: {transcript[:100]}...")
        return transcript

    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None
