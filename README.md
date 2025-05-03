## Tutorial: Setting Up Producer and Consumer Services

This tutorial will guide you through the setup and running of two Python.py applications: a producer service and a consumer service. The producer service provides recipe data, and the consumer service fetches this data from the producer and returns it to the client. We will also cover installing dependencies, running the applications, and testing the setup.

## Table of Content
- [Prerequisites](#prerequisites)
- [Step 1: Setting Up The Producer Service](#step-1-setting-up-the-producer-service)
- [Step 2: Setting Up The Consumer Service](#step-2-setting-up-the-consumer-service)
- [Step 3: Testing The Setup](#step-3-testing-the-setup)
- [Step 4: Dockerise The Application](#step-4-dockerize-the-application)

## Prerequisites

- Python installed on your machine (download from [python.org](https://www.python.org/))
- pip (comes with Python) or PyPI

___

### Step 1: Setting Up the Producer Service

1. **Create a Directory for the Producer**

   ```bash
   mkdir producer
   cd producer
   ```

2. **Install Dependencies**

   ```bash
   pip install fastapi
   ```

3. **Create the Producer Script**

   Create a file named `producer.py` and add the following code:

   ```javascript
   #!/usr/bin/env node

   const server = require('fastify')();
   const HOST = process.env.HOST || '127.0.0.1';
   const PORT = process.env.PORT || 4000;

   console.log(`worker pid=${process.pid}`);

   server.get('/recipes/:id', async (req, reply) => {
       console.log(`worker request pid=${process.pid}`);
       const id = Number(req.params.id);
       if (id !== 42) {
           reply.statusCode = 404;
           return { error: 'not_found' };
       }
       return {
           producer_pid: process.pid,
           recipe: {
               id, name: "Chicken Tikka Masala",
               steps: "Throw it in a pot...",
               ingredients: [
                   {id: 1, name: "Chicken", quantity: "1 lb", },
                   {id: 2, name: "Sauce", quantity: "2 cups", }
               ]
           }
       };
   });

   server.listen(PORT, HOST, () => {
       console.log(`Producer running at http://${HOST}:${PORT}`);
   });
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

   Create a file named `consumer.js` and add the following code:

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

### Conclusion

You have successfully set up and run both the producer and consumer services. The producer provides recipe data, and the consumer fetches and returns this data. This setup demonstrates basic microservice communication using Python and FastAPI.

### Additional Notes

- You can customize the host, port, and target by setting the `HOST`, `PORT`, and `TARGET` environment variables.
- To stop the services, you can use `Ctrl+C` in the terminal where they are running.
- Ensure both services are running simultaneously to test the consumer properly.