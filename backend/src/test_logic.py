import logic


def test_consumption_per_category():
    appliances: list[logic.Appliance] = [
        "fridge",
        "freezer",
        "washing_machine",
        "tv",
        "small_light",
    ]
    consumption = logic._average_consumption_per_category(appliances)
    assert consumption == {"F": 2250.0, "A": 1500.0, "L": 300.0}


def test_duplicate_appliance():
    """Test that the function works with duplicate appliances."""
    appliances: list[logic.Appliance] = ["fridge", "fridge"]
    categories = logic._average_consumption_per_category(appliances)
    assert categories == {"F": 2000.0}


def test_appliances_to_energy_single():
    """Simple case with only a fridge"""
    appliances: list[logic.Appliance] = ["fridge"]
    on_hours = 7
    total_consumption = 2000 * on_hours

    assert logic.appliances_to_energy(appliances, total_consumption) == {
        "fridge": total_consumption
    }


def test_appliances_to_energy_mixed_same_category():
    """Simple case with two appliances of the same category"""
    appliances: list[logic.Appliance] = ["fridge", "freezer"]
    on_hours = 7
    consumption_fridge = 2000 * on_hours / 2
    consumption_freezer = 2500 * on_hours / 2
    total_consumption = consumption_fridge + consumption_freezer

    assert logic.appliances_to_energy(appliances, total_consumption) == {
        "fridge": consumption_fridge,
        "freezer": consumption_freezer,
    }


def test_appliances_to_energy_mixed_categories():
    """Simple case with two appliances of the same category"""
    appliances: list[logic.Appliance] = ["fridge", "tv"]
    on_hours_cat_f = 8
    consumption_fridge = 2000.0 * on_hours_cat_f
    on_hours_cat_l = 23
    consumption_tv = 500.0 * on_hours_cat_l

    # Add 1 as we will not have the exact total consumption
    total_consumption = consumption_fridge + consumption_tv + 1

    assert logic.appliances_to_energy(appliances, total_consumption) == {
        "fridge": consumption_fridge,
        "tv": consumption_tv,
    }


def test_appliances_to_energy_duplicate_items():
    """Simple case with two appliances of the same category"""
    appliances: list[logic.Appliance] = ["fridge", "fridge", "dishwasher", "tv"]
    on_hours_cat_f = 8
    consumption_fridge = 2000.0 * on_hours_cat_f
    on_hours_cat_a = 4
    consumption_dishwasher = 2500.0 * on_hours_cat_a
    on_hours_cat_l = 24
    consumption_tv = 500.0 * on_hours_cat_l

    # Add 1 as we will not have the exact total consumption
    total_consumption = consumption_fridge + consumption_dishwasher + consumption_tv + 1

    assert logic.appliances_to_energy(appliances, total_consumption) == {
        "fridge": consumption_fridge,
        "dishwasher": consumption_dishwasher,
        "tv": consumption_tv,
    }


def test_impossible_combination():
    """Simple case with two appliances of the same category"""
    assert (
        logic.appliances_to_energy(["fridge", "fridge", "dishwasher", "tv"], 1) is None
    )
