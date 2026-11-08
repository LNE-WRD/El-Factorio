from dataclasses import dataclass, field

QUALITY = {"normal": 1.0, "uncommon": 1.3, "rare": 1.6, "epic": 1.9, "legendary": 2.5}

@dataclass
class AssemblingMachine:
    tier: int = 1
    quality: str = "normal"
    modules: list = field(default_factory=list)

STATS = {1: (0.5, 0), 2: (0.75, 2), 3: (1.25, 4)}   # tier: (speed, slots)

def __post_init__(self):
    if len(self.modules) > self.slots:
        raise ValueError(f"{self.name} only has {self.slots} module slots")

    @property
    def name(self):
        return f"assembling-machine-{self.tier}"

    @property
    def speed(self):
        return self.STATS[self.tier][0]

    @property
    def slots(self):
        return self.STATS[self.tier][1]

    @property
    def categories(self):
        if self.tier == 1:
            return ("crafting", "advanced-crafting")
        return ("crafting", "advanced-crafting", "crafting-with-fluid")

    @property
    def effective_speed(self):
        multiplier = max(0.2, 1 + sum(m.speed for m in self.modules))
        return self.speed * QUALITY[self.quality] * multiplier

    @property
    def effective_prod(self):
        return sum(m.prod for m in self.modules)

    @property
    def effective_pollution(self):
        return sum(m.pollution for m in self.modules)

    @property
    def effective_energy(self):
        return sum(m.energy for m in self.modules)
