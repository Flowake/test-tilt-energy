from typing import Literal, Callable
from collections import defaultdict
from itertools import product


type Category = Literal["F"] | Literal["A"] | Literal["L"]

type Appliance = Literal["fridge"] | Literal["washing_machine"] | Literal[
    "tv"
] | Literal["freezer"] | Literal["dishwasher"] | Literal["induction_stove"] | Literal[
    "small_light"
] | Literal[
    "big_light"
]

CATEGORIES = ("A", "F", "L")

CONSUMPTION: dict[Appliance, int] = {
    "fridge": 2000,
    "washing_machine": 1500,
    "tv": 500,
    "freezer": 2500,
    "dishwasher": 2500,
    "induction_stove": 3000,
    "small_light": 100,
    "big_light": 800,
}

CATEGORY_USAGE: dict[Category, Callable[[], list[int]]] = {
    "A": lambda: list(range(1, 5)),
    "F": lambda: list(range(6, 9)),
    "L": lambda: list(range(4, 25)),
}


def _appliance_to_category(appliance: Appliance) -> Category:
    match appliance:
        case "fridge" | "freezer":
            return "F"
        case "washing_machine" | "dishwasher" | "induction_stove":
            return "A"
        case "tv" | "small_light" | "big_light":
            return "L"


def _count_appliances_per_category(appliances: list[Appliance]) -> dict[Category, int]:
    categories_count = defaultdict(int)
    for appliance in appliances:
        category = _appliance_to_category(appliance)
        categories_count[category] += 1
    return categories_count


def _average_consumption_per_category(
    appliances: list[Appliance],
) -> dict[Category, float]:
    """Compute the average consumption per categories.

    If a category is not present, it will not be in the output.
    """
    categories_count = _count_appliances_per_category(appliances)
    categories_consumption = defaultdict(int)
    for appliance in appliances:
        category = _appliance_to_category(appliance)
        categories_consumption[category] += CONSUMPTION[appliance]
    return {
        cat: (categories_consumption[cat] / categories_count[cat])
        for cat in CATEGORIES
        if categories_count[cat] > 0
    }


def _on_hours_to_energy(
    on_hours: tuple[int, ...],
    categories: list[Category],
    consumption: dict[Category, float],
) -> float:
    """Map the ON hours to the total energy consumption."""
    return sum(
        on * consumption[cat] for on, cat in zip(on_hours, categories, strict=True)
    )


def appliances_to_energy(
    appliances: list[Appliance], total_consumption: float
) -> dict[Appliance, float] | None:
    categories_count = _count_appliances_per_category(appliances)
    existing_categories = sorted(categories_count.keys())
    average_consumption = _average_consumption_per_category(
        appliances,
    )

    # As the search space is small, we can afford to compute
    # the cartesian product of all possible combinations and test
    # them all to find the best one.
    #
    # In a real case scenario, I would have used an optimisation algorithm
    # from scipy for example to minimize the difference with the total consumption.
    combinations = {
        on_product: _on_hours_to_energy(
            on_product, existing_categories, average_consumption
        )
        for on_product in product(
            *[CATEGORY_USAGE[cat]() for cat in existing_categories]
        )
    }
    # We do not keep combinations that are above the total consumption.
    combinations = {
        on_product: consumption
        for on_product, consumption in combinations.items()
        if consumption <= total_consumption
    }

    if len(combinations) == 0:
        return None

    # Find the combination that give the closest consumption to the total consumption
    on_hours_per_categories = min(
        combinations.items(),
        key=lambda x: total_consumption - x[1],
    )[0]

    # As the ON hours are split between the appliances of the same category,
    # we compute the average ON hours per category per appliance.
    on_hours_per_appliance_cat = {
        cat: on / categories_count[cat]
        for on, cat in zip(on_hours_per_categories, existing_categories)
    }

    # We the ON hours and the known consumption for each appliance,
    # we can compute the total consumption for each appliance.
    #
    # We need to handle the case where an appliance is present multiple times.
    consumption_per_appliance: dict[Appliance, float] = {
        appliance: 0.0 for appliance in set(appliances)
    }

    for appliance in appliances:
        consumption_per_appliance[appliance] += (
            on_hours_per_appliance_cat[_appliance_to_category(appliance)]
            * CONSUMPTION[appliance]
        )
    return consumption_per_appliance
