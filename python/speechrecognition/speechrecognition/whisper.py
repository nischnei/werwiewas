from pathlib import Path
from typing import Optional

import whisper
# Working around to fix a whisper Future warning
import functools
whisper.torch.load = functools.partial(whisper.torch.load, weights_only=True)


class WhisperRecognition:
    def __init__(self, model_name: str = "small"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, path: Path, initial_prompt: Optional[str]=None):
        result = self.model.transcribe(path, initial_prompt=initial_prompt, fp16=False)
        return result["text"]