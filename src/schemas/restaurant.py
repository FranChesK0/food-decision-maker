from pydantic import BaseModel, ConfigDict


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
