from backend.backend import MLBackend

app = MLBackend()

# Entry point to run the server
def main():
    import uvicorn

    # Start the server
    uvicorn.run("backend.server:app", host="127.0.0.1", port=8000, reload=True)