from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import json
import os
import logging

app = FastAPI()
DATA_FILE = "external_trades.json"
logging.basicConfig(level=logging.INFO)

@app.post("/upload")
async def upload_data(request: Request):
    try:
        data = await request.json()
        logging.info(f"✅ Received JSON: {data}")
        
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)  # Save with formatting for easy debug
        
        return {"status": "✅ File saved successfully"}
    except Exception as e:
        logging.error(f"❌ Error saving data: {e}")
        return {"error": str(e)}

@app.get("/external_trades.json")
def get_data():
    if os.path.exists(DATA_FILE):
        return FileResponse(DATA_FILE, media_type="application/json")
    return {"error": "File not found"}
