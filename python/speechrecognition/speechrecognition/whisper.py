from pathlib import Path
import whisper


class WhisperRecognition:
    def __init__(self, model_name="small"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, path: Path):
        result = self.model.transcribe(path)
        return result["text"]