from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from config import PlayerConfig, load_config, save_config
from media_player import MediaPlayer


class SettingsUI:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path
        self.config = load_config(config_path) if config_path else load_config()
        self.player = MediaPlayer(self.config)

        self.root = tk.Tk()
        self.root.title("RGB Loop Player Settings")
        self._build_layout()
        if self.config.autoplay:
            self.player.start()

    def _build_layout(self) -> None:
        self.root.geometry("480x320")
        padding = {"padx": 10, "pady": 5}

        tk.Label(self.root, text="Cílová složka s médii").grid(row=0, column=0, sticky="w", **padding)
        self.media_dir_var = tk.StringVar(value=self.config.media_dir)
        tk.Entry(self.root, textvariable=self.media_dir_var, width=40).grid(row=1, column=0, columnspan=2, sticky="we", **padding)
        tk.Button(self.root, text="Vybrat složku", command=self._choose_folder).grid(row=1, column=2, **padding)

        self.autoplay_var = tk.BooleanVar(value=self.config.autoplay)
        tk.Checkbutton(self.root, text="Autoplay při startu", variable=self.autoplay_var).grid(row=2, column=0, sticky="w", **padding)

        self.shuffle_var = tk.BooleanVar(value=self.config.shuffle)
        tk.Checkbutton(self.root, text="Náhodné pořadí", variable=self.shuffle_var).grid(row=3, column=0, sticky="w", **padding)

        tk.Label(self.root, text="Hlasitost (0-100)").grid(row=4, column=0, sticky="w", **padding)
        self.volume_var = tk.IntVar(value=self.config.volume)
        tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.volume_var).grid(row=5, column=0, columnspan=2, sticky="we", **padding)

        tk.Label(self.root, text="Zpoždění mezi položkami (s)").grid(row=6, column=0, sticky="w", **padding)
        self.delay_var = tk.DoubleVar(value=self.config.loop_delay)
        tk.Scale(self.root, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.delay_var).grid(row=7, column=0, columnspan=2, sticky="we", **padding)

        tk.Button(self.root, text="Uložit nastavení", command=self._save_config).grid(row=8, column=0, **padding)
        tk.Button(self.root, text="Zastavit", command=self._stop_playback).grid(row=8, column=1, **padding)
        tk.Button(self.root, text="Spustit/Obnovit", command=self._start_playback).grid(row=8, column=2, **padding)

        self.status_label = tk.Label(self.root, text="Status: připraveno")
        self.status_label.grid(row=9, column=0, columnspan=3, sticky="w", **padding)

        self.playlist_box = tk.Listbox(self.root, height=8, width=60)
        self.playlist_box.grid(row=10, column=0, columnspan=3, sticky="we", **padding)
        self._refresh_playlist_box()

    def _refresh_playlist_box(self) -> None:
        self.playlist_box.delete(0, tk.END)
        for item in self.player.playlist():
            self.playlist_box.insert(tk.END, item.name)

    def _choose_folder(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.media_dir_var.get() or ".")
        if selected:
            self.media_dir_var.set(selected)

    def _save_config(self) -> None:
        self.config.media_dir = self.media_dir_var.get()
        self.config.autoplay = bool(self.autoplay_var.get())
        self.config.shuffle = bool(self.shuffle_var.get())
        self.config.volume = int(self.volume_var.get())
        self.config.loop_delay = float(self.delay_var.get())
        save_config(self.config, self.config_path) if self.config_path else save_config(self.config)
        self.player.refresh_playlist()
        self.player.set_volume(self.config.volume)
        self._refresh_playlist_box()
        self.status_label.config(text="Status: nastavení uloženo")

    def _start_playback(self) -> None:
        self._save_config()
        self.player.start()
        self.status_label.config(text="Status: přehrávání běží")

    def _stop_playback(self) -> None:
        self.player.stop()
        self.status_label.config(text="Status: přehrávání zastaveno")

    def run(self) -> None:
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.player.stop()
            messagebox.showinfo("Media Player", "Aplikace byla ukončena.")


def launch_settings() -> None:
    ui = SettingsUI()
    ui.run()


if __name__ == "__main__":
    launch_settings()
