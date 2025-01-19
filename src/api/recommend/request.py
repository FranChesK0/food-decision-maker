from pydantic import BaseModel


class RecommendRequest(BaseModel):
    """
    Request for recommendation.

    Args:
        cuisine (str): Cuisine.
        budget (float): Budget.
    """

    cuisine: str
    budget: float
