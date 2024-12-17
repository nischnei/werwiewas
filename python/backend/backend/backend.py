"""Backend for ML speech and text generation interaction."""

import tempfile
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, UploadFile
from homepageparser.beautifulsoup import BeautifulsoupParser
from rag.llmware import LlmwareRag
from speechrecognition.whisper import WhisperRecognition


class MLBackend:
    """App deriving from FastAPI controlling http protocol."""

    def __init__(self):
        """Define variables, initialization is done on startup."""
        super().__init__()
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
        self.homepage_parser = BeautifulsoupParser()

    def init_rag(self):
        """Initialize Retrieval Augmented Generator."""
        self.rag = LlmwareRag()


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
            return {"answer": response.encode('utf-8')}
