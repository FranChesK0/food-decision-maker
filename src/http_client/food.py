from loguru import logger
from async_lru import alru_cache

from core import settings
from schemas import Menu, Category, Restaurant

from .base import HTTPClient


class FoodHTTPClient(HTTPClient):
    """
    Food HTTP client.

    Args:
        base_url (str): The base URL of the HTTP server.

    Methods:
        get_restaurants() -> list[Restaurant]: Get a list of all restaurants.
        get_categories() -> list[Category]: Get a list of all categories.
        get_restaurants_by_category(category_id: int) -> list[Restaurant]: Get
            a list of restaurants by category.
        get_menu(restaurant_id: int) -> Menu: Get the menu of a restaurant.
    """

    def __init__(self) -> None:
        super().__init__(base_url=settings.FOOD_DELIVERY_BASE_URL)

    @logger.catch
    @alru_cache
    async def get_restaurants(self) -> list[Restaurant]:
        """
        Get a list of all restaurants.

        Returns:
            list[Restaurant]: A list of all restaurants.
        """
        async with self._session.get("/restaurants") as response:
            data = await response.json()
        return [Restaurant.model_validate(r) for r in data]

    @logger.catch
    @alru_cache
    async def get_categories(self) -> list[Category]:
        """
        Get a list of all categories.

        Returns:
            list[Category]: A list of all categories.
        """
        async with self._session.get("/category") as response:
            data = await response.json()
        return [Category.model_validate(c) for c in data]

    @logger.catch
    @alru_cache
    async def get_restaurants_by_category(self, category_id: int) -> list[Restaurant]:
        """
        Get a list of restaurants by category.

        Args:
            category_id (int): The id of the category.

        Returns:
            list[Restaurant]: A list of restaurants.
        """
        async with self._session.get(f"/category/{category_id}/restaurants") as response:
            data = await response.json()
        return [Restaurant.model_validate(r) for r in data]

    @logger.catch
    @alru_cache
    async def get_menu(self, restaurant_id: int) -> Menu:
        """
        Get the menu of a restaurant.

        Args:
            restaurant_id (int): The id of the restaurant.

        Returns:
            Menu: The menu of the restaurant.
        """
        async with self._session.get(f"/menu/{restaurant_id}/composition") as response:
            data = await response.json()
        return Menu.model_validate(data)
