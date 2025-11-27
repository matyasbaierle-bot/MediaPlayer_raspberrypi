from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG_PATH = Path("config.json")


@dataclass
class PlayerConfig:
    media_dir: str = "media"
    autoplay: bool = True
    shuffle: bool = False
    volume: int = 80  # 0-100
    loop_delay: float = 0.2  # seconds between items when looping

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "PlayerConfig":
        config = cls()
        for field_name in asdict(config).keys():
            if field_name in data:
                setattr(config, field_name, data[field_name])
        return config


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> PlayerConfig:
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            return PlayerConfig.from_json(json.load(handle))
    return PlayerConfig()


def save_config(config: PlayerConfig, path: Path = DEFAULT_CONFIG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(config.to_json(), handle, indent=2)
        handle.write("\n")
