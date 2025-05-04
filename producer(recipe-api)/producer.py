# pip install fastapi
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import uvicorn

app = FastAPI()

HOST = os.getenv('HOST', '127.0.0.1')  # Get HOST env var or default to localhost
PORT = int(os.getenv('PORT', 4000))   # Get PORT env var or default to 4000

print(f"Server will run on http://{HOST}:{PORT}")
# Get the process ID of the current process
pid = os.getpid()

print(f"Worker pid = {pid}")

recipe = [{
        "producer_pid": os.getpid(),
        "recipe": {
            "id": id,
            "name": "Chicken Tikka Masala",
            "steps": "Throw it in a pot...",
            "ingredients": [
                {"id": 1, "name": "Chicken", "quantity": "1 lb"},
                {"id": 2, "name": "Sauce", "quantity": "2 cups"},
            ],
        },
    }]

@app.get("/recipes/{id}")
async def recipes(id: int):
    print(f"Worker pid = {pid}")
    
    if id != 42:
        raise HTTPException(status_code=404, detail="not_found")
    
    recipe = [{
        "producer_pid": os.getpid(),
        "recipe": {
            "id": id,
            "name": "Chicken Tikka Masala",
            "steps": "Throw it in a pot...",
            "ingredients": [
                {"id": 1, "name": "Chicken", "quantity": "1 lb"},
                {"id": 2, "name": "Sauce", "quantity": "2 cups"},
            ],
        },
    }]
    return recipe

if __name__ == "__main__":
    print(f"Producer running at http://{HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)