from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import List, Dict, Any

app = FastAPI(title="External Trades Mirroring API", version="1.0")

# تمكين CORS للسماح بطلبات من أي مصدر (يمكن تقييدها لاحقاً)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# تخزين البيانات في الذاكرة
trades_data: List[Dict[str, Any]] = []
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload")
async def upload_data(request: Request):
    """
    استقبال بيانات الصفقات من MetaTrader وحفظها في الذاكرة
    """
    global trades_data
    
    try:
        data = await request.json()
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Expected a JSON array")
        
        trades_data = data
        logger.info(f"✅ تم استقبال {len(data)} صفقة، أحدث تذكرة: {data[0]['ticket'] if data else 'N/A'}")
        
        return JSONResponse(
            content={"status": "success", "received_trades": len(data)},
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"❌ خطأ في استقبال البيانات: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/external_trades.json")
def get_data():
    """
    إرجاع بيانات الصفقات المخزنة في الذاكرة
    """
    if not trades_data:
        logger.warning("⚠️ لم يتم استقبال أي بيانات بعد")
        return JSONResponse(
            content={"error": "No data available", "status": "pending"},
            status_code=404
        )
    
    logger.info(f"📤 إرسال {len(trades_data)} صفقة إلى العميل")
    return JSONResponse(
        content=trades_data,
        status_code=200
    )

@app.get("/status")
def check_status():
    """
    نقطة فحص لحالة السيرفر
    """
    return {
        "status": "running",
        "trades_count": len(trades_data),
        "latest_ticket": trades_data[0]["ticket"] if trades_data else None,
        "memory_usage": f"{len(str(trades_data))/1024:.2f} KB"
    }

# يمكنك إضافة هذه للتحكم في وقت تشغيل السيرفر
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
