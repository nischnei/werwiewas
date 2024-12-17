"""Speech recognition with openai's Whisper."""
# Working around to fix a whisper Future warning
import functools
from pathlib import Path
from typing import Optional

import whisper

whisper.torch.load = functools.partial(whisper.torch.load, weights_only=True)


class WhisperRecognition:
    """Defines the WhisperRecognition class for speech recognition."""

    def __init__(self, model_name: str = "small"):
        """Construct the class."""
        self.model = whisper.load_model(model_name)

    def transcribe(self, path: Path, initial_prompt: Optional[str] = None) -> str:
        """Transcribe an audio file from path and return the text."""
        result = self.model.transcribe(path, initial_prompt=initial_prompt, fp16=False)
        return result["text"]
