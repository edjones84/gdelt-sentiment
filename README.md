# GDELT Search term sentiment

This project provides a basic front-end interface to interact with the query endpoint of a FastAPI server.
It allows users to submit queries to a GDELT API and receive sentiment analysis scores for the corresponding query responses.

## Prerequisites

Before running the front-end, ensure that you have the following installed:

- FastAPI server (already set up and running)

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/your-username/gdelt-sentiment.git
   ```

2. Navigate to the project directory:

   ```shell
   cd gdelt-sentiment
   ```

3. Install the http server :

   ```shell
   npm install -g http-server
   ```
   
4. Start the FastAPI server in the root of the directory 
   
   ```shell
   uvicorn main:app --reload  
   ```

5. Start the http server in the /frontend directory 

   ```shell
   http-server 
   ```

6. Navigate to http://192.168.1.203:8080/ and query away!

## Usage

1. Open the `index.html` file in a web browser or host the project files on a web server.

2. Enter a query in the input field and click the "Submit" button.

3. The front-end will send a POST request to the query endpoint of the FastAPI server, passing the query as the request payload.

4. The response from the server will be displayed below the form, providing sentiment analysis scores and other details related to the query response.

## API Endpoint

The front-end interacts with the following API endpoint:

- Endpoint: `/query`
- Method: get
- Request Payload: JSON object with a single property `queryInput` containing the query string.
- Response Format: JSON object with the following properties:
  - `neg`: float - Negative sentiment score
  - `neu`: float - Neutral sentiment score
  - `pos`: float - Positive sentiment score
  - `compound`: float - Compound sentiment score
  - `original_title`: str - Original title of the response
  - `title`: str - Title of the response
  - `origin_language`: str - Language of the response

Ensure that the FastAPI server is up and running and that the endpoint is accessible at `http://localhost:8000/`.

## Testing

This code utilises Cucumber for BDD and integration testing, ensure the FASTAPI endpoint is up and running before running the following command in the tests directory:

```bash
behave
```