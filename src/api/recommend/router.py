from fastapi import APIRouter

from schemas import RecommendedSet
from decision import FoodOrderingEngine

from .request import RecommendRequest
from .response import RecommendResponse

router = APIRouter(prefix="/recommend", tags=["Decision Making"])


@router.post("", summary="Recommend menu")
async def recommend_menu(request: RecommendRequest) -> RecommendedSet | RecommendResponse:
    engine = FoodOrderingEngine()
    restaurants = await engine.choose_restaurants(request.cuisine)

    recommendations: list[RecommendedSet] = []
    for restaurant in restaurants:
        recommendation = await engine.choose_menu(restaurant.id, request.budget)
        if recommendation is not None:
            recommendations.append(recommendation)

    if recommendations:
        return recommendations[0]
    return RecommendResponse(msg="No recommendations found")
