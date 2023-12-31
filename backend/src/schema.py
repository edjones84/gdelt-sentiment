from pydantic import BaseModel


class Article(BaseModel):
    url: str
    url_mobile: str
    original_title: str
    title: str
    seendate: str
    socialimage: str
    domain: str
    language: str
    sourcecountry: str


Article.update_forward_refs()


class Articles(BaseModel):
    articles: list[Article]


class QueryResponse(BaseModel):
    neg: float
    neu: float
    pos: float
    compound: float
    original_title: str
    title: str
    origin_language: str


QueryResponse.update_forward_refs()


class QueryResponses(BaseModel):
    scores: list[QueryResponse]
