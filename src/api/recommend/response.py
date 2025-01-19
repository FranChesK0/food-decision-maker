from pydantic import BaseModel


class RecommendResponse(BaseModel):
    msg: str
