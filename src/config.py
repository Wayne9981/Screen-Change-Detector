import json
from dataclasses import dataclass, fields, asdict


def dataclass_from_dict(cls, d: dict):
    try:
        field_types = {f.name: f.type for f in fields(cls)}
        return cls(**{f: dataclass_from_dict(field_types[f], v) for f, v in d.items()})
    except TypeError:
        return d


@dataclass
class Hotkeys:
    screen_analysis: str
    periodic_screen_analysis: str
    setting_config: str


@dataclass
class Config:
    image_folder: str
    diff_threshold_percentage: int
    time_interval_sec: float
    analysis_minutes: int
    screen_shot_area: list[int]
    hotkeys: Hotkeys

    @classmethod
    def from_dict(cls, d) -> "Config":
        return dataclass_from_dict(cls, d)


class ConfigAccessor:
    def __init__(self):
        with open("config.json") as f:
            cfg = json.load(f)
        self.cfg = Config.from_dict(cfg)

    def save(self):
        cfg = asdict(self.cfg)
        with open("config.json", "w") as f:
            json.dump(cfg, f, indent=4)
            f.write("\n")
