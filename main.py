from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import List, Dict, Any
import json

app = FastAPI(title="External Trades Mirroring API", version="1.0")

# تمكين CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تخزين البيانات
trades_data: List[Dict[str, Any]] = []
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload")
async def upload_data(request: Request):
    global trades_data
    try:
        raw_data = await request.body()
        logger.info(f"📥 Raw data received: {raw_data.decode()}")
        
        data = json.loads(raw_data)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array")
            
        trades_data = data
        logger.info(f"✅ Received {len(data)} trades")
        return {"status": "success", "count": len(data)}
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON decode error: {str(e)}")
        raise HTTPException(400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(400, detail=str(e))

@app.get("/external_trades.json")
def get_data():
    return trades_data if trades_data else {"error": "No data available"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
