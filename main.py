from fastapi import FastAPI
import uvicorn

from gdelt_api import make_request, extract_titles, sentiment_dictionary_gen
from schema import QueryResponses

app = FastAPI()


@app.post("/query")
def query_endpoint(query_request: str) -> QueryResponses:
    response_json = make_request(query_request)
    titles = extract_titles(response_json)
    scores_out = sentiment_dictionary_gen(titles)
    return scores_out

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
