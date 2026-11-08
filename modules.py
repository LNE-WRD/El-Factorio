from dataclasses import dataclass, field

@dataclass(frozen=True)
class Module:
    name:      str
    speed:     float = 0.0
    prod:      float = 0.0
    energy:    float = 0.0
    pollution: float = 0.0
    quality:   float = 0.0

SPEED_1 = Module("speed-1", speed=0.2, energy=0.5)
SPEED_2 = Module("speed-2", speed=0.3, energy=0.6)
SPEED_3 = Module("speed-3", speed=0.5, energy=0.7)

PROD_1  = Module("prod-1", speed=-0.15, prod=0.04, energy=0.4, pollution=0.3)
PROD_2  = Module("prod-2", speed=-0.15, prod=0.06, energy=0.6, pollution=0.4)
PROD_3  = Module("prod-3", speed=-0.15, prod=0.10, energy=0.8, pollution=0.5)

EFF_1   = Module("eff-1", energy=-0.3)
EFF_2   = Module("eff-2", energy=-0.4)
EFF_3   = Module("eff-3", energy=-0.5)

QUAL_1  = Module("qual-1", speed=-0.05, quality=0.01)
QUAL_2  = Module("qual-2", speed=-0.05, quality=0.02)
QUAL_3  = Module("qual-3", speed=-0.05, quality=0.025)