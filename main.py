from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()
DATA_FILE = "external_trades.json"

@app.post("/upload")
async def upload_data(request: Request):
    data = await request.json()
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    return {"status": "✅ File saved successfully"}

@app.get("/external_trades.json")
def get_data():
    if os.path.exists(DATA_FILE):
        return FileResponse(DATA_FILE)
    return {"error": "File not found"}
