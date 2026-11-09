from dataclasses import dataclass, field
from math import ceil

MINING_TIME = {"iron-ore": 1, "copper-ore": 1, "coal": 1, "stone": 1}
RESOURCE_DRAIN = {"normal": 1.0, "uncommon": 0.83, "rare": 0.66, "epic": 0.5, "legendary": 0.16}

@dataclass(frozen=True)
class Drill:
    name: str
    speed: float
    power: float
    pollution: float
    slots: int = 0
    resource_drain: float = 1.0

BURNER_DRILL   = Drill("burner-drill", 0.25, 150, 12)
ELECTRIC_DRILL = Drill("elec-drill", 0.5, 90, 10, slots=3)
BIG_DRILL      = Drill("big-drill", 2.5, 300, 40, slots=4, resource_drain=0.5)


@dataclass(frozen=True)
class MiningResult:
    ore: float
    ore_depleted: float     # ce qui disparaît réellement du gisement
    drills: int
    energy_mj: float
    pollution: float


@dataclass
class MiningDrill:
    model: Drill
    modules: list = field(default_factory=list)
    quality: str = "normal"
    research_lvl: float = 0.0

    def __post_init__(self):
        if self.quality not in RESOURCE_DRAIN:
            raise ValueError(f"Qualité inconnue : {self.quality}")
        if len(self.modules) > self.model.slots:
            raise ValueError(f"{self.model.name} n'a que {self.model.slots} slot(s) de module")

    def _multiplier(self, stat):
        return max(0.2, 1 + sum(getattr(m, stat) for m in self.modules))

    @property
    def speed(self):
        return self.model.speed * self._multiplier("speed")

    @property
    def productivity(self):
        return sum(m.prod for m in self.modules) + 0.1 * self.research_lvl

    def produce(self, ore, quantity, seconds):
        if ore not in MINING_TIME:
            raise ValueError(f"Ressource inconnue : {ore}")
        if quantity <= 0 or seconds <= 0:
            raise ValueError("La quantité et le temps doivent être positifs")

        operations = quantity / (1 + self.productivity)
        work_seconds = operations * MINING_TIME[ore] / self.speed
        energy = self._multiplier("energy")
        pollution_rate = self.model.pollution_per_min * energy * self._multiplier("pollution")

        return MiningResult(
            ore=quantity,
            ore_depleted=operations * self.model.resource_drain * RESOURCE_DRAIN[self.quality],
            drills=ceil(work_seconds / seconds),
            energy_mj=self.model.power_kw * energy * work_seconds / 1000,
            pollution=pollution_rate * work_seconds / 60,
        )
