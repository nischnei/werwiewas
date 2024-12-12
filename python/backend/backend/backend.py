from fastapi import FastAPI, File, UploadFile
from time import sleep
import tempfile

from speechrecognition.whisper import WhisperRecognition

class MLBackend(FastAPI):
    def __init__(self):
        super().__init__()
        self.is_initialized = False
        self.resource_data = None

        # Register routes
        self.add_api_route("/status", self.get_status, methods=["GET"])
        self.add_api_route("/process-audio/", self.process_audio, methods=["POST"])

        # Register events
        self.on_event("startup")(self.startup_event)
        self.on_event("shutdown")(self.shutdown_event)

        # Model
        self.speech_recognition = None

    async def get_status(self):
        """
        Endpoint to check if the server is initialized.
        """
        if self.is_initialized:
            return {"status": "ready", "data": self.resource_data}
        else:
            return {"status": "initializing"}

    async def startup_event(self):
        """
        Lifecycle event to handle app startup logic.
        """
        print("Starting initialization...")
        # Simulate some heavy initialization
        self.speech_recognition = WhisperRecognition()
        self.resource_data = "Important Resource Loaded"
        self.is_initialized = True
        print("Initialization complete.")

    async def shutdown_event(self):
        """
        Lifecycle event to handle app shutdown logic.
        """
        pass

    
    async def process_audio(self, file: UploadFile = File(...)):
        # Temporary save the audio file locally
        with tempfile.NamedTemporaryFile() as tmp:
            content = await file.read()
            tmp.write(content)
            # transcribe the audio
            transcribed_text = self.speech_recognition.transcribe(tmp.name)

        # Response with dummy content for now
        return {"message": transcribed_text}