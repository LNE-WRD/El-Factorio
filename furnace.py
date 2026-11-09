from dataclasses import dataclass, field
from primary.modules import QUALITY
from math import ceil

@dataclass
class FurnaceModel:
    name: str
    speed: float
    power_kw: float
    pollution_per_minutes: float
    slots: int = 0
    drain_kw: float = 0.0

STONE_FURNACE = FurnaceModel("stone-furnace", 1, 90, 2)
STEEL_FURNACE = FurnaceModel("steel-furnace", 2, 90, 4)
ELEC_FURNACE  = FurnaceModel("elec-furnace", 2, 180, 1, slots=2, drain_kw=6)

@dataclass
class ProductionResult:
    outputs: float
    crafts: float
    inputs: dict
    furnaces: int
    energy_mj: float
    pollution: float

@dataclass
class Furnace:
    model: FurnaceModel
    modules: list = field(default_factory=list)
    quality: str = "normal"

    def __post_init__(self):
        if self.quality not in QUALITY:
            raise ValueError(f"Qualité inconnue : {self.quality}")
        if len(self.modules) > self.model.slots :
            raise ValueError(f"{self.model.name} ne possède que {self.model.slots} slot(s) de module.")
    
    def _multiplier(self, stat):
        return max(0.2, 1 + sum(getattr(m, stat) for m in self.modules))

    @property
    def speed(self):
        return self.model.speed * self._multiplier("speed") * QUALITY[self.quality]

    @property
    def productivity(self):
        return sum(m.prod for m in self.modules)

    def produce(self, recipe, quantity, seconds):
        if recipe.category != "smelting":
            raise ValueError(f"{self.model.name} ne peut pas fabriquer {recipe.name}")
        if quantity <= 0 or seconds <= 0:
            raise ValueError("La quantitié et le temps doivent être positifs")

        crafts = quantity/(recipe.output_qty * (1 + self.productivity))

        work_seconds = crafts * recipe.time/self.speed
        furnaces = ceil(work_seconds/seconds)

        energy = self.multiplier("energy")
        active_kj = self.model.power_kw * energy * work_seconds
        drain_kj = self.model.drain_kw * furnaces * seconds

        pollution_per_minute = self.model.pollution_per_minutes * energy * self._multiplier("pollution")

        return ProductionResult(
            outputs=quantity,
            crafts=crafts,
            inputs={item: qty * crafts for item, qty in recipe.inputs.item()},
            furnaces=furnaces,
            energy_mj=(active_kj + drain_kj)/1000,
            pollution=pollution_per_minute * work_seconds/60,
        )
