from pydantic import BaseModel, ConfigDict

from .category import Category


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


class RecommendedSet(BaseModel):
    """
    A recommended set of items.

    Args:
        restaurant_id (int): The id of the restaurant.
        items (list[Item]): The items of the recommended set.
        total_price (float): The total price of the recommended set.
    """

    restaurant_id: int
    items: list[Item]
    total_price: float

    model_config = ConfigDict(from_attributes=True)
