# pip install fastapi uvicorn
from fastapi import FastAPI, HTTPException
import os
import uvicorn

app = FastAPI()

HOST = os.getenv('HOST', '127.0.0.1') 
PORT = int(os.getenv('PORT', 4000))  

# Get the process ID of the current process
pid = os.getpid()

@app.get("/recipes/{id}")
async def recipes(id: int):
    print(f"Worker pid = {pid}")
    
    if id != 42:
        raise HTTPException(status_code=404, detail="not_found")
    
    recipe = [{
        "producer_pid": pid,
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