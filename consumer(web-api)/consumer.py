# pip install fastapi requests uvicorn
from fastapi import FastAPI
import os
import uvicorn
import requests
import json

app = FastAPI()

HOST = os.getenv('HOST', '127.0.0.1') 
PORT = int(os.getenv('PORT', 3000))  
TARGET = os.getenv('TARGET', 'localhost:4000') 

@app.get("/")
async def recipes():
    req = requests.get(f"http://{TARGET}/recipe/42")
    producer_data = req.json()

    return [{
        "producer_pid": os.getpid(),
        "producer_data": producer_data
    }]    

if __name__ == "__main__":
    print(f"Consumer running at http://{HOST}:{PORT}")
    print(requests.get(f"http://{TARGET}/recipe/42"))
    uvicorn.run(app, host=HOST, port=PORT)