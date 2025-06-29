from fastapi import FastAPI

app = FastAPI(title="Core Dispatch 2.0 API")


@app.get("/")
def read_root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "Core Dispatch 2.0 API is running."}
