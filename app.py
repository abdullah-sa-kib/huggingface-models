from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from PIL import Image
import io

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer hf_your_api_key_here"}  # Replace with your API key

class Prompt(BaseModel):
    inputs: str

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error generating image")
    return response.content

@app.post("/generate")
async def generate_image(prompt: Prompt):
    image_bytes = query({"inputs": prompt.inputs})
    return {"image_data": image_bytes.hex()}
