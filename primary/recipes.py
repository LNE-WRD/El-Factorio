from dataclasses import dataclass

@dataclass(frozen=True)          # frozen = can't be modified by accident
class Recipe:
    name: str
    time: float        # seconds per craft at crafting speed 1
    inputs: dict       # {"iron-ore": 1}
    output: str
    output_qty: float
    category: str      # which kind of machine can make it

IRON_PLATE = Recipe("iron-plate", 3.2, {"iron-ore": 1}, "iron-plate", 1, "smelting")
CAST_IRON  = Recipe("casting-irong", 3.2, {"molten-iron": 20}, "iron-plate", 2, "metallurgy")

COPPER_PLATE = Recipe("copper-plate", 3.2, {"copper-ore": 1}, "copper-plate", 1, "smelting")
CAST_COPPER = Recipe("copper-plate", 3.2, {"copper-ore": 20}, "copper-plate", 2, "metallurgy")