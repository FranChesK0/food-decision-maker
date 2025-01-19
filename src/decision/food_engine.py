from loguru import logger
from experta import MATCH, Fact, Rule, KnowledgeEngine  # type: ignore[import-untyped]

from schemas import Item, Menu, MenuItem, Restaurant, RecommendedSet
from http_client import FoodHTTPClient

from .utils import check_match, filter_menu_by_buget


class FoodOrderingEngine(KnowledgeEngine):  # type: ignore[no-any-unimported]
    """
    A knowledge engine for ordering food.

    Methods:
        choose_restaurants(cuisine: str) -> list[Restaurant]: Choose restaurants
            based on cuisine.
        choose_menu(restaurant_id: int, budget: float) -> RecommendedSet | None:
            Choose menu based on budget.
    """

    @Rule(Fact(action="order_food"), Fact(cuisine=MATCH.cuisine))
    async def choose_restaurants(self, cuisine: str) -> list[Restaurant]:
        """
        Choose restaurants based on cuisine.

        Args:
            cuisine (str): The cuisine.

        Returns:
            list[Restaurant]: A list of restaurants.
        """
        async with FoodHTTPClient() as client:
            restaurants = await client.get_restaurants()

        cuisines: list[str] = []
        for r in restaurants:
            cuisines.extend(r.cuisines)

        matched_cuisine = check_match(cuisine, cuisines)
        logger.debug(matched_cuisine)
        return [r for r in restaurants if matched_cuisine in r.cuisines]

    @Rule(
        Fact(action="order_food"),
        Fact(restaurant_id=MATCH.restaurant_id),
        Fact(budget=MATCH.budget),
    )
    async def choose_menu(
        self, restaurant_id: int, budget: float
    ) -> RecommendedSet | None:
        """
        Choose menu based on budget.

        Args:
            restaurant_id (int): The id of the restaurant.
            budget (float): The budget.

        Returns:
            RecommendedSet | None: The recommended set of items.
        """
        async with FoodHTTPClient() as client:
            menu = await client.get_menu(restaurant_id)
        categories: list[MenuItem] = []
        for category in menu.items:
            items: list[Item] = []
            for item in category.items:
                if item.price <= budget:
                    items.append(item)
            if items:
                categories.append(MenuItem(category=category.category, items=items))
        if not categories:
            return None

        recommendations = filter_menu_by_buget(
            Menu(restaurant_id=restaurant_id, items=categories), budget
        )
        if not recommendations:
            return None

        async with FoodHTTPClient() as client:
            restaurants = await client.get_restaurants()
        restaurant_title = [r.title for r in restaurants if r.id == restaurant_id][0]

        recommended_set = recommendations[0]
        return RecommendedSet(
            restaurant_id=restaurant_id,
            restaurant_title=restaurant_title,
            items=list(recommended_set),
            total_price=sum(item.price for item in recommended_set),
        )
