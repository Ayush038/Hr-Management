from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as agent_router
from routes.booking import router as booking_router
from routes.computer_use import router as computer_router
import os

load_dotenv()


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router)
app.include_router(booking_router)
app.include_router(computer_router)

@app.get("/")
def message():
    return {"message": "Welcome to the HR Management API"}