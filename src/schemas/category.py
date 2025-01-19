from pydantic import BaseModel, ConfigDict


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
