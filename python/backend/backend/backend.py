"""Backend for ML speech and text generation interaction."""

import os
import tempfile
from contextlib import asynccontextmanager

import yaml
from fastapi import FastAPI, File, Form, UploadFile
from homepageparser.factory import HomepageParserFactory
from pydantic import BaseModel
from rag.factory import RagFactory
from speechrecognition.whisper import WhisperRecognition


class MLBackendConfig(BaseModel):
    """Stores the backend configuration."""

    speech_recognition: str
    homepage_parser: str
    rag: str


class MLBackend:
    """App deriving from FastAPI controlling http protocol."""

    def __init__(self):
        """Define variables, initialization is done on startup."""
        super().__init__()
        # Get the config from the WWW_BACKEND_CONFIG env variable or use the default.
        cfg_path = os.environ.get(
            "WWW_BACKEND_CONFIG", os.path.join(os.path.dirname(__file__), "config", "whisper_bs_llmware.yaml")
        )
        with open(cfg_path, "r") as file:
            config_data = yaml.safe_load(file)
        self.cfg = MLBackendConfig(**config_data)

        self.app = FastAPI(lifespan=self.lifespan)
        self.is_initialized = False
        self.resource_data = None

        # Model
        self.speech_recognition = None

        # Rag
        self.rag = None

        # Homepageparser
        self.homepage_parser = None

        # register routes
        self.register_routes()

    def init_speech_recognition(self):
        """Init the speech recongition."""
        self.speech_recognition = WhisperRecognition()

    def init_homepage_parser(self):
        """Initialize homepage parser."""
        self.homepage_parser = HomepageParserFactory.get(self.cfg.homepage_parser)

    def init_rag(self):
        """Initialize Retrieval Augmented Generator."""
        self.rag = RagFactory.get(self.cfg.rag)

    @asynccontextmanager
    async def lifespan(self, _):
        """Manage startup and teardown behavior using lifespan."""
        # Moving this to separate function so this can later be mocked.
        self.init_speech_recognition()
        self.init_homepage_parser()
        self.init_rag()

        self.is_initialized = True

        yield

        # Shutdown should go here, but we have nothing to shutdown currently.

    def register_routes(self):
        """Register routes with decorators."""

        @self.app.post("/process-audio/")
        async def process_audio(file: UploadFile = File(...), url: str = Form(...)):
            """Step 1: Transcribe audio to question."""
            with tempfile.NamedTemporaryFile() as tmp:
                content = await file.read()
                tmp.write(content)
                helper_prompt = f"Tell me something about {url}."
                question = self.speech_recognition.transcribe(path=tmp.name, initial_prompt=helper_prompt)
            return {"question": question}

        @self.app.post("/process-url/")
        async def process_url(url: str = Form(...)):
            """Step 2: Fetch homepage content."""
            homepage_content = self.homepage_parser.parse(url)
            return {"homepage": homepage_content}

        @self.app.post("/process-rag/")
        async def process_rag(homepage: str = Form(...), query: str = Form(...)):
            """Step 3: Generate an answer using RAG."""
            response = self.rag.query_context(context=homepage, query=query)
            return {"answer": response.encode("utf-8")}
