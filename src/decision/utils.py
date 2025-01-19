import itertools

from rapidfuzz import process

from schemas import Item, Menu

MEAL_REQUIREMENTS: dict[str, list[str]] = {
    "main": [
        "Горячие блюда",
        "Горячее",
        "Пицца",
        "Паста",
        "Стейки",
        "Супы",
        "Суши",
        "Роллы",
    ],
    "side": ["Салаты", "Закуски", "Стрит фуд", "Гарниры", "Соусы"],
    "drink": ["Напитки"],
    "dessert": ["Десерты"],
}


def check_match(user_input: str, options: list[str], threshold: float = 75) -> str:
    """
    Check if the user input matches any of the options with a given threshold.

    Args:
        user_input (str): The user input.
        options (list[str]): The options to check.
        threshold (float, optional): The threshold for matching. Defaults to 75.

    Returns:
        str: The matched option, or an empty string if no match is found.
    """
    match, score, _ = process.extractOne(user_input, options)
    if score >= threshold:
        return match
    return ""


def filter_menu_by_buget(menu: Menu, budget: float) -> list[tuple[Item, ...]]:
    """
    Filter the menu by budget.

    Args:
        menu (Menu): The menu to filter.
        budget (float): The budget.

    Returns:
        list[list[Item]]: The filtered menu.
    """
    grouped_items: dict[str, list[Item]] = {}
    for menu_item in menu.items:
        for item in menu_item.items:
            grouped_items.setdefault(menu_item.category.name, []).append(item)
    available_requirements: dict[str, list[str]] = {
        component: [cat for cat in categories if cat in grouped_items]
        for component, categories in MEAL_REQUIREMENTS.items()
    }
    valid_components: dict[str, list[Item]] = {
        component: grouped_items[categories[0]]
        for component, categories in available_requirements.items()
        if categories
    }

    valid_combinations: list[tuple[Item, ...]] = []
    for combination in itertools.product(*valid_components.values()):
        total_cost = sum(item.price for item in combination)
        if total_cost <= budget:
            valid_combinations.append(combination)
    return valid_combinations
