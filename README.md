## Tutorial: Setting Up Producer and Consumer Services

This tutorial will guide you through the setup and running of two Python.py applications: a producer service and a consumer service. The producer service provides recipe data, and the consumer service fetches this data from the producer and returns it to the client. We will also cover installing dependencies, running the applications, and testing the setup.

## Table of Content
- [Prerequisites](#prerequisites)
- [Step 1: Setting Up The Producer Service](#step-1-setting-up-the-producer-service)
- [Step 2: Setting Up The Consumer Service](#step-2-setting-up-the-consumer-service)
- [Step 3: Testing The Setup](#step-3-testing-the-setup)
- [Step 4: Containerize The Application](#step-4-containerize-the-application)

## Prerequisites

- Python installed on your machine (download from [python.org](https://www.python.org/))
- pip (comes with Python) or PyPI
- Docker Desktop installed on your machine (download from [docker.com](https://www.docker.com/products/docker-desktop/))

___

### Step 1: Setting Up the Producer Service

1. **Create a Directory for the Producer**

   ```bash
   mkdir producer
   cd producer
   ```

2. **Install Dependencies**

   ```bash
   pip install fastapi uvicorn
   ```

3. **Create the Producer Script**

   Create a file named `producer.py` and add the following code:

    ```python
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    import os
    import uvicorn

    app = FastAPI()

    HOST = os.getenv('HOST', '127.0.0.1')  
    PORT = int(os.getenv('PORT', 4000))   

    pid = os.getpid()

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
    ```

4. **Run the Producer Service**

   ```bash
   python3 producer.py
   ```

   You should see output indicating the producer is running.

### Step 2: Setting Up the Consumer Service

1. **Create a Directory for the Consumer**

   ```bash
   mkdir ../consumer
   cd ../consumer
   ```

2. **Install Dependencies**

   ```bash
   pip install fastapi & requests@2.32
   ```

3. **Create the Consumer Script**

   Create a file named `consumer.py` and add the following code:

   ```javascript
   #!/usr/bin/env node

   const server = require('fastify')();
   const fetch = require('node-fetch');
   const HOST = process.env.HOST || '127.0.0.1';
   const PORT = process.env.PORT || 3000;
   const TARGET = process.env.TARGET || 'localhost:4000';

   server.get('/', async () => {
       const req = await fetch(`http://${TARGET}/recipes/42`);
       const producer_data = await req.json();

       return {
           consumer_pid: process.pid,
           producer_data
       };
   });

   server.listen(PORT, HOST, () => {
       console.log(`Consumer running at http://${HOST}:${PORT}/`);
   });
   ```

4. **Run the Consumer Service**

   ```bash
   python3 consumer.py
   ```

   You should see output indicating the consumer is running.

### Step 3: Testing the Setup

1. **Test the Producer Service**

   Open a web browser or use `curl` to access the producer service:

   ```bash
   curl http://127.0.0.1:4000/recipes/42
   ```

   You should receive a JSON response with the recipe details:

   ```json
   {
       "producer_pid": 12345,
       "recipe": {
           "id": 42,
           "name": "Chicken Tikka Masala",
           "steps": "Throw it in a pot...",
           "ingredients": [
               {"id": 1, "name": "Chicken", "quantity": "1 lb"},
               {"id": 2, "name": "Sauce", "quantity": "2 cups"}
           ]
       }
   }
   ```

2. **Test the Consumer Service**

   Open a web browser or use `curl` to access the consumer service:

   ```bash
   curl http://127.0.0.1:3000/
   ```

   You should receive a JSON response that includes the data fetched from the producer service:

   ```json
   {
       "consumer_pid": 12345,
       "producer_data": {
           "producer_pid": 12345,
           "recipe": {
               "id": 42,
               "name": "Chicken Tikka Masala",
               "steps": "Throw it in a pot...",
               "ingredients": [
                   {"id": 1, "name": "Chicken", "quantity": "1 lb"},
                   {"id": 2, "name": "Sauce", "quantity": "2 cups"}
               ]
           }
       }
   }
   ```

### Step 4: Containerize The Application

1. **Create a Directory for the Containers**

   ```bash
   mkdir containerize
   cd containerize
   ```

2. **Create Dockerfiles**

   Create a file named `requirements.txt` with the required dependencies and add the following code:

   ```
   fastapi
   uvicorn
   requests
   ```

   Create a file named `Dockerfile-producer` and add the following code:

   ```DOCKERFILE
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt . 
   COPY producer.py .
   
   RUN pip install --no-cache-dir -r requirements.txt
   
   EXPOSE 80
   
   CMD ["python", "producer.py", "--port", "80"]
   ```

   Create another file named `Dockerfile-consumer` and add the following code:
   
   ```DOCKERFILE
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt . 
   COPY consumer.py .
   
   RUN pip install --no-cache-dir -r requirements.txt
   
   EXPOSE 81
   
   CMD ["python", "consumer.py", "--port", "81"]
   ```

3. **Copy Producer & Consumer files to Containerize**

   ```bash
   cp /'producers(recipe-api)'/producer.py /containerize/
   ```
   ```bash
   cp /'consumers(web-api)'/producer.py /containerize/
   ```

3. **Build & Run Docker Images**

   ```bash
   docker build -f Dockerfile-producer -t producer .
   ```
   ```sh
   docker run -p 4000:80 producer
   ```
   ```bash
   docker build -f Dockerfile-consumer -t consumer .
   ```
   ```sh
   docker run -p 3000:81 consumer
   ```

### Step 5: Create Helm Chart

### Conclusion

You have successfully set up and run both the producer and consumer services. The producer provides recipe data, and the consumer fetches and returns this data. This setup demonstrates basic microservice communication using Python and FastAPI.

### Additional Notes

- You can customize the host, port, and target by setting the `HOST`, `PORT`, and `TARGET` environment variables.
- To stop the services, you can use `Ctrl+C` in the terminal where they are running.
- Ensure both services are running simultaneously to test the consumer properly.