import json

from fastapi import FastAPI, Query
import uvicorn
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from backend.src.gdelt_api import make_request, extract_titles, sentiment_dictionary_gen
from backend.src.schema import QueryResponses

app = FastAPI()

origins = [
    "*"  # Add the origin that's making the request
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "This is the initial Fast api implementation"}


@app.get("/endpoint", response_model=QueryResponses)
def query_endpoint(queryInput: str = Query(..., alias="queryInput")) -> Response:
    response_json = make_request(queryInput)
    titles = extract_titles(response_json)
    scores_out = sentiment_dictionary_gen(titles)
    return jsonable_encoder(json.loads(scores_out.json()))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
