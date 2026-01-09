from fastapi import FastAPI
from backend.api.market import router as market_router
from backend.api.market import router as market_router
from backend.api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="Market Price & Harvest Logistics Planner",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(market_router)
app.include_router(market_router)
app.include_router(chat_router)

@app.get("/")
def health_check():
    return {"status": "running"}
