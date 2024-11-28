# Backend application 

from fastapi import FastAPI, WebSocket
from app.routers import real_time_main
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
	title = "Meeting Translation API",
	description = "API for real-tume meeting transcription",
	version = "1.0.0"
	)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers to manage API endpoints (instance of FastAPI APIRouter) 
# The goal is to introduce modular router based endpoints to handle and process data

app.include_router(real_time_main.router)
#app.include_router(transcription.router)
#app.include_router(translation.router)