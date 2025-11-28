from __future__ import annotations

import random
import threading
import time
from pathlib import Path
from typing import Iterable, List

import vlc

from config import PlayerConfig

SUPPORTED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav", ".flac", ".jpg", ".jpeg", ".png", ".bmp"}


class MediaPlayer:
    """Simple looping media player built on python-vlc."""

    def __init__(self, config: PlayerConfig) -> None:
        self.config = config
        self._playlist: List[Path] = []
        self._position = 0
        self._instance = vlc.Instance()
        self._player = self._instance.media_player_new()
        self._player.audio_set_volume(self.config.volume)
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @staticmethod
    def _iter_media_files(media_dir: Path) -> Iterable[Path]:
        if not media_dir.exists():
            return []
        for item in sorted(media_dir.iterdir()):
            if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield item

    def refresh_playlist(self) -> None:
        media_dir = Path(self.config.media_dir)
        items = list(self._iter_media_files(media_dir))
        if self.config.shuffle:
            random.shuffle(items)
        self._playlist = items
        self._position = 0

    def _play_media(self, media_path: Path) -> None:
        media = self._instance.media_new(str(media_path))
        self._player.set_media(media)
        self._player.play()

    def _loop(self) -> None:
        while not self._stop_event.is_set():
            with self._lock:
                if not self._playlist:
                    time.sleep(0.5)
                    continue
                media_path = self._playlist[self._position]
                self._position = (self._position + 1) % len(self._playlist)
            self._play_media(media_path)
            time.sleep(self.config.loop_delay)
            # Wait for playback to finish or stop event
            while self._player.is_playing() and not self._stop_event.is_set():
                time.sleep(0.2)

    def start(self) -> None:
        self.refresh_playlist()
        self._stop_event.clear()
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._player.stop()
        if self._thread:
            self._thread.join(timeout=1)

    def toggle_pause(self) -> None:
        self._player.pause()

    def set_volume(self, volume: int) -> None:
        volume = max(0, min(100, volume))
        self.config.volume = volume
        self._player.audio_set_volume(volume)

    def is_playing(self) -> bool:
        return bool(self._player.is_playing())

    def playlist(self) -> List[Path]:
        return list(self._playlist)
