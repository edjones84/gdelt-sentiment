from pydantic import BaseModel


class Article(BaseModel):
    url: str
    url_mobile: str
    title: str
    seendate: str
    socialimage: str
    domain: str
    language: str
    sourcecountry: str


class Articles(BaseModel):
    articles: list[Article]


class QueryResponse(BaseModel):
    neg: float
    neu: float
    pos: float
    compound: float
    title: str
    origin_language: str


class QueryResponses(BaseModel):
    scores: list[QueryResponse]