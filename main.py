from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config import load_config, save_config
from media_player import MediaPlayer
from settings_ui import launch_settings


def run_headless(config_path: Path | None = None) -> None:
    config = load_config(config_path) if config_path else load_config()
    save_config(config, config_path) if config_path else save_config(config)
    player = MediaPlayer(config)
    player.start()
    print("Media player spuštěn. Stiskněte Ctrl+C pro ukončení.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        player.stop()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RGB loop media player pro Raspberry Pi 4/5")
    parser.add_argument("--headless", action="store_true", help="Spustí přehrávač bez GUI (na kioskový displej)")
    parser.add_argument("--config", type=Path, help="Cesta k JSON konfiguraci", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])
    if args.headless:
        run_headless(args.config)
    else:
        launch_settings()


if __name__ == "__main__":
    main()
