# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os

from pydantic import BaseModel

from app.swagger.swagger_loader import load_swagger_from_file, extract_endpoints

app = FastAPI(title="Swagger Endpoint Extractor (MVP)")


@app.get("/sample")
def sample():
    return {"message": "Upload a swagger file via /upload-swagger (POST multipart/form-data)"}



class SwaggerInput(BaseModel):
    swagger_path: str
    users: int = 10
    spawn_rate: int = 2
    run_time: str = "10s"

@app.post("/upload-swagger")
async def upload_swagger(data: SwaggerInput):
    """
    Accepts Swagger file path and load test configuration as JSON.
    Example request:
    {
        "swagger_path": "/Users/dharmendrapr/Desktop/AUTOGEN/ApiLoadTesting/demo.json",
        "users": 10,
        "spawn_rate": 2,
        "run_time": "10s"
    }
    """
    if not os.path.exists(data.swagger_path):
        raise HTTPException(status_code=400, detail=f"Swagger file not found: {data.swagger_path}")

    # For testing, just return the received input
    return {
        "message": "Swagger file path received successfully",
        "swagger_path": data.swagger_path,
        "config": {
            "users": data.users,
            "spawn_rate": data.spawn_rate,
            "run_time": data.run_time
        }
    }