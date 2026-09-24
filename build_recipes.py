"""Build the transcribed recipe data from the 13 reference pages.

Run: python build_recipes.py
The photos are private reference material and must never be added to the repo.
"""

import json
from pathlib import Path


def layer(ingredient, quantity=1, unit="piece", each_ml=None, placement=None, preparation=None):
    item = {"ingredient": ingredient, "quantity": quantity, "unit": unit}
    if each_ml is not None:
        item["amountPerApplicationMl"] = each_ml
    if placement:
        item["placement"] = placement
    if preparation:
        item["preparation"] = preparation
    return item


def bun(kind, part, preparation=None):
    return layer(f"bun_{kind}_{part}", preparation=preparation)


def sauce(kind, times, ml):
    return layer(f"sauce_{kind}", times, "application", each_ml=ml)


def r(id, name, page, category, *layers):
    return {"id": id, "name": name, "sourcePage": page, "category": category,
            "layers": list(layers)}


R = [
    # Page 51: Upper muffin half is already buttered.
    r("mcmuffin_fresh_chicken", "McMuffin Fresh Chicken", 51, "breakfast",
      bun("mcmuffin", "oberteil", "buttered"), layer("patty_chicken_tempura"),
      layer("cheese_standard"), layer("tomate", 1, "slice"),
      layer("eisbergsalat", 10, "g"), sauce("sandwich", 1, 10),
      bun("mcmuffin", "unterteil")),
    r("mcmuffin_egg", "McMuffin Egg", 51, "breakfast",
      bun("mcmuffin", "oberteil", "buttered"), layer("round_egg"),
      layer("cheese_standard"), bun("mcmuffin", "unterteil")),
    r("mcmuffin_bacon_egg", "McMuffin Bacon & Egg", 51, "breakfast",
      bun("mcmuffin", "oberteil", "buttered"), layer("bacon_streifen", 2, "strip"),
      layer("round_egg"), layer("cheese_standard"), bun("mcmuffin", "unterteil")),

    # Page 52: McToast Bacon & Cheese adds bacon above the same cheese arrangement.
    r("mcmuffin_sausage_egg", "McMuffin Sausage & Egg", 52, "breakfast",
      bun("mcmuffin", "oberteil", "buttered"), layer("round_egg"),
      layer("patty_sausage"), layer("cheese_standard"), bun("mcmuffin", "unterteil")),
    r("mctoast_cheese", "McToast Cheese", 52, "breakfast",
      bun("hamburger", "oberteil"), layer("cheese_standard", 2, placement="star"),
      bun("hamburger", "unterteil")),
    r("mctoast_bacon_cheese", "McToast Bacon & Cheese", 52, "breakfast",
      bun("hamburger", "oberteil"), layer("bacon_streifen", 3, "strip"),
      layer("cheese_standard", 2, placement="star"), bun("hamburger", "unterteil")),

    # Page 53: 1 portion of scrambled egg corresponds to 1.5 eggs.
    r("mcwrap_ruehrei_bacon", "McWrap Rührei Bacon", 53, "breakfast_wrap",
      layer("ruehrei", 1, "portion", preparation="1.5 eggs per portion"),
      layer("cheese_standard_half", 2, "half_slice"),
      layer("bacon_streifen", 3, "strip"), layer("eisbergsalat", 20, "g"),
      layer("crispy_onions", 3, "g"), layer("sauce_breakfast", 20, "g"),
      layer("wrap_tortilla")),
    r("mcwrap_ruehrei_cheese", "McWrap Rührei Cheese", 53, "breakfast_wrap",
      layer("ruehrei", 1, "portion", preparation="1.5 eggs per portion"),
      layer("cheese_standard", 2), layer("tomate", 2, "slice"),
      layer("eisbergsalat", 20, "g"), layer("sauce_breakfast", 20, "g"),
      layer("wrap_tortilla")),

    # Pages 54-55: Seeded bun appears with Unterteil at the top of the diagram.
    r("big_morning_chicken", "Big Morning Chicken", 54, "breakfast",
      bun("koernerbroetchen", "unterteil"), layer("patty_chicken_tempura"),
      layer("cheese_standard"), layer("tomate", 2, "slice"),
      layer("eisbergsalat", 12.5, "g"), sauce("sandwich", 2, 10),
      bun("koernerbroetchen", "oberteil")),
    r("big_morning_farmer", "Big Morning Farmer", 54, "breakfast",
      bun("koernerbroetchen", "unterteil"), layer("patty_sausage"),
      layer("bacon_streifen", 3, "strip"), layer("cheese_standard"),
      layer("tomate", 2, "slice"), layer("eisbergsalat", 12.5, "g"),
      sauce("sandwich", 2, 10), bun("koernerbroetchen", "oberteil")),
    r("big_morning_egg", "Big Morning Egg", 55, "breakfast",
      bun("koernerbroetchen", "unterteil"), layer("round_egg"),
      layer("cheese_standard"), layer("tomate", 2, "slice"),
      layer("eisbergsalat", 12.5, "g"), layer("sauce_breakfast", 20, "g"),
      bun("koernerbroetchen", "oberteil")),
    r("hamburger", "Hamburger", 55, "burger",
      bun("hamburger", "unterteil"), layer("patty_beef_10_1"),
      layer("salzgurke", 1, "slice"), sauce("ketchup", 1, 10),
      layer("sauce_senf", 0.79, "g"), bun("hamburger", "oberteil")),
    r("cheeseburger", "Cheeseburger", 55, "burger",
      bun("hamburger", "unterteil"), layer("patty_beef_10_1"),
      layer("cheese_standard"), layer("salzgurke", 1, "slice"),
      sauce("ketchup", 1, 10), layer("sauce_senf", 0.79, "g"),
      bun("hamburger", "oberteil")),

    # Page 56: Beef 10:1 is pre-onioned; never add a fresh-onion layer here.
    r("double_cheeseburger", "Double Cheeseburger", 56, "burger",
      bun("hamburger", "unterteil"), layer("patty_beef_10_1"),
      layer("cheese_standard", placement="star"), layer("patty_beef_10_1"),
      layer("cheese_standard"), layer("salzgurke", 2, "slice"),
      sauce("ketchup", 1, 10), layer("sauce_senf", 0.79, "g"),
      bun("hamburger", "oberteil")),
    r("mcdouble_chili_cheese", "McDouble Chili Cheese", 56, "burger",
      bun("hamburger", "unterteil"), layer("patty_beef_10_1"),
      layer("cheese_standard"), layer("patty_beef_10_1"),
      layer("jalapenos", 3, "slice"), layer("sauce_hot_chili_cheese", 20, "g"),
      bun("hamburger", "oberteil")),

    # Page 57: The Big Mac has two separate sauce/lettuce levels and a middle bun.
    r("big_mac", "Big Mac", 57, "burger",
      bun("big_mac", "oberteil"), layer("patty_beef_10_1"),
      layer("salzgurke", 2, "slice"), layer("eisbergsalat", 12.5, "g"),
      sauce("big_mac", 1, 15), bun("big_mac", "mittelteil"),
      layer("patty_beef_10_1"), layer("cheese_standard"),
      layer("eisbergsalat", 12.5, "g"), sauce("big_mac", 1, 15),
      bun("big_mac", "unterteil")),
    r("big_tasty_bacon", "Big Tasty Bacon", 57, "burger",
      bun("big_tasty", "unterteil"), layer("cheese_standard", 2),
      layer("patty_beef_3_1"), layer("bacon_streifen", 3, "strip"),
      layer("cheese_standard"), layer("tomate", 2, "slice"),
      layer("eisbergsalat", 28, "g"),
      layer("zwiebeln_frisch_weiss", 10, "g"), sauce("big_tasty", 3, 10),
      bun("big_tasty", "oberteil")),

    # Page 58: Double variants add their boxed layers immediately below Unterteil.
    r("hamburger_royal_cheese", "Hamburger Royal Cheese", 58, "burger",
      bun("hamburger_royal", "unterteil"), layer("cheese_standard", placement="star"),
      layer("patty_beef_4_1"), layer("cheese_standard"),
      layer("salzgurke", 2, "slice"), layer("zwiebeln_frisch_weiss", 7, "g"),
      sauce("ketchup", 1, 15), layer("sauce_senf", 0.79, "g"),
      bun("hamburger_royal", "oberteil")),
    r("double_hamburger_royal_cheese", "Double Hamburger Royal Cheese", 58, "burger",
      bun("hamburger_royal", "unterteil"), layer("patty_beef_4_1"),
      layer("cheese_standard", placement="star"), layer("patty_beef_4_1"),
      layer("cheese_standard"), layer("salzgurke", 2, "slice"),
      layer("zwiebeln_frisch_weiss", 7, "g"), sauce("ketchup", 1, 15),
      layer("sauce_senf", 0.79, "g"), bun("hamburger_royal", "oberteil")),
    r("hamburger_royal_ts", "Hamburger Royal TS", 58, "burger",
      bun("hamburger_royal", "unterteil"), layer("patty_beef_4_1"),
      layer("cheese_standard"), layer("tomate", 2, "slice"),
      layer("eisbergsalat", 12.5, "g"),
      layer("zwiebeln_frisch_weiss", 7, "g"), sauce("sandwich", 2, 10),
      bun("hamburger_royal", "oberteil")),
    r("double_hamburger_royal_ts", "Double Hamburger Royal TS", 58, "burger",
      bun("hamburger_royal", "unterteil"), layer("patty_beef_4_1"),
      layer("cheese_standard", placement="star"), layer("patty_beef_4_1"),
      layer("cheese_standard"), layer("tomate", 2, "slice"),
      layer("eisbergsalat", 12.5, "g"),
      layer("zwiebeln_frisch_weiss", 7, "g"), sauce("sandwich", 2, 10),
      bun("hamburger_royal", "oberteil")),

    # Page 59: Filet-o-Fish bun is steamed on both halves.
    r("double_beef_classic", "Double Beef Classic", 59, "burger",
      bun("hamburger_royal", "unterteil"), sauce("big_tasty", 1, 10),
      layer("patty_beef_10_1"), layer("patty_beef_10_1"),
      layer("eisbergsalat", 12.5, "g"), layer("salzgurke", 2, "slice"),
      sauce("honig_senf", 2, 10), bun("hamburger_royal", "oberteil")),
    r("filet_o_fish", "Filet-o-Fish", 59, "burger",
      bun("hamburger", "unterteil", "steamed"),
      layer("cheese_standard_half", 1, "half_slice"),
      layer("patty_filet_o_fish"), sauce("tartar", 1, 20),
      bun("hamburger", "oberteil", "steamed")),

    # Page 60: McChicken uses McRib bun, as explicitly confirmed.
    r("mcrib", "McRib", 60, "burger",
      bun("mcrib", "unterteil"),
      layer("patty_pork_mcrib", preparation="marinated with approximately 40 g Western/McRib sauce in UHC"),
      layer("salzgurke", 2, "slice"), layer("zwiebeln_frisch_weiss", 7, "g"),
      bun("mcrib", "oberteil")),
    r("mcchicken_classic", "McChicken Classic", 60, "burger",
      bun("mcrib", "unterteil"), layer("patty_chicken_classic"),
      layer("eisbergsalat", 12.5, "g"), sauce("sandwich", 2, 10),
      bun("mcrib", "oberteil")),

    # Page 61: The second Chicken Tempura patty is an inserted Double layer.
    r("mccrispy", "McCrispy", 61, "burger",
      bun("mccrispy", "unterteil"), layer("patty_mccrispy"),
      layer("cheese_standard"), layer("eisbergsalat", 12.5, "g"),
      sauce("honig_senf", 2, 10), bun("mccrispy", "oberteil")),
    r("chickenburger", "Chickenburger", 61, "burger",
      bun("hamburger", "unterteil"), layer("patty_chicken_tempura"),
      layer("eisbergsalat", 10, "g"), sauce("sweet_chili", 1, 12),
      bun("hamburger", "oberteil")),
    r("double_chickenburger", "Double Chickenburger", 61, "burger",
      bun("hamburger", "unterteil"), layer("patty_chicken_tempura"),
      layer("patty_chicken_tempura"), layer("eisbergsalat", 10, "g"),
      sauce("sweet_chili", 1, 12), bun("hamburger", "oberteil")),

    # Page 62: Two half patties mean one patty cut in half, not two whole patties.
    r("mcwrap_chicken_honig_senf", "McWrap Chicken Honig-Senf", 62, "wrap",
      layer("patty_chicken_classic_half", 2, "half_patty"),
      layer("cheese_standard_half", 2, "half_slice"),
      layer("tomate", 2, "slice"), layer("eisbergsalat", 25, "g"),
      sauce("honig_senf", 1, 10), sauce("sandwich", 2, 10),
      layer("wrap_tortilla")),
    r("mcwrap_veggie_honig_senf", "McWrap Veggie Honig-Senf", 62, "wrap",
      layer("patty_veggie_half", 2, "half_patty"),
      layer("cheese_standard_half", 2, "half_slice"),
      layer("tomate", 2, "slice"), layer("eisbergsalat", 25, "g"),
      sauce("honig_senf", 1, 10), sauce("sandwich", 2, 10),
      layer("wrap_tortilla")),

    # Page 63: McVeggie TS adds cheese and tomato relative to McVeggie.
    r("mcveggie_ts", "McVeggie TS", 63, "burger",
      bun("hamburger_royal", "unterteil"), layer("patty_veggie"),
      layer("cheese_standard"), layer("tomate", 2, "slice"),
      layer("eisbergsalat", 12.5, "g"), sauce("sandwich", 2, 10),
      bun("hamburger_royal", "oberteil")),
    r("mcveggie", "McVeggie", 63, "burger",
      bun("hamburger_royal", "unterteil"), layer("patty_veggie"),
      layer("eisbergsalat", 12.5, "g"), sauce("sandwich", 2, 10),
      bun("hamburger_royal", "oberteil")),
]


DATA = {
    "schemaVersion": 1,
    "sourcePages": "51-63",
    "orientation": "Each layers array follows the printed diagram from top to bottom; products are prepared upside down.",
    "quantityConvention": "A sauce with unit=application has quantity applications, each of amountPerApplicationMl. Other quantities use the stated unit.",
    "recipes": R,
}


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    target = root / "data" / "recipes.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assets = root / "assets" / "ingredients"
    assert len(R) == 32, len(R)
    assert len({recipe["id"] for recipe in R}) == len(R)
    for recipe in R:
        assert 51 <= recipe["sourcePage"] <= 63
        for item in recipe["layers"]:
            assert (assets / (item["ingredient"] + ".png")).is_file(), (recipe["id"], item["ingredient"])
            assert item["quantity"] > 0
    print(f"Wrote {len(R)} recipes; every layer has an ingredient PNG.")
