from loguru import logger
from pydantic import BaseModel, ConfigDict
from async_lru import alru_cache

from .base import HTTPClient


class Restaurant(BaseModel):
    """
    Restaurant schema.

    Args:
        id (int): The id of the restaurant.
        title (str): The title of the restaurant.
        address (str): The address of the restaurant.
        cuisines (list[str]): The cuisines of the restaurant.
    """

    id: int
    title: str
    address: str
    cuisines: list[str]

    model_config = ConfigDict(from_attributes=True)


class Category(BaseModel):
    """
    Category schema.

    Args:
        id (int): The id of the category.
        name (str): The name of the category.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Item(BaseModel):
    """
    Item schema.

    Args:
        id (int): The id of the item.
        restaurant_id (int): The id of the restaurant.
        category_id (int): The id of the category.
        name (str): The name of the item.
        price (float): The price of the item.
        description (str): The description of the item.
    """

    id: int
    restaurant_id: int
    category_id: int
    name: str
    price: float
    description: str

    model_config = ConfigDict(from_attributes=True)


class MenuItem(BaseModel):
    """
    MenuItem schema.

    Args:
        category (Category): The category of the menu item.
        items (list[Item]): The items of the menu item.
    """

    category: Category
    items: list[Item]

    model_config = ConfigDict(from_attributes=True)


class Menu(BaseModel):
    """
    Menu schema.

    Args:
        restaurant_id (int): The id of the restaurant.
        items (list[MenuItem]): The items of the menu.
    """

    restaurant_id: int
    items: list[MenuItem]

    model_config = ConfigDict(from_attributes=True)


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

    def __init__(self, base_url: str) -> None:
        super().__init__(base_url=base_url)

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
