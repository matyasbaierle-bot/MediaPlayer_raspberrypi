# RGB Loop Media Player (Raspberry Pi 4/5)

Jednoduchý přehrávač pro Raspberry Pi, který na smyčku (loop) přehrává obrázky a videa ze zadané složky. Obsahuje GUI pro nastavení (Tkinter), umí startovat automaticky (autoplay) a používá knihovnu `python-vlc`, takže zvládá většinu běžných formátů.

## Rychlá instalace (student-friendly)

1. **Připravte Raspberry Pi** (OS Lite nebo Desktop). Aktualizujte balíčky:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. **Nainstalujte VLC a Python závislosti**:
   ```bash
   sudo apt install -y vlc python3-pip python3-tk
   pip3 install -r requirements.txt
   ```
3. **Zkopírujte projekt** (např. přes Git nebo ZIP):
   ```bash
   git clone https://github.com/<váš-účet>/MediaPlayer_raspberrypi.git
   cd MediaPlayer_raspberrypi
   ```
4. **Přidejte média** do složky `media/` (lze změnit v UI). Podporované přípony: mp4, mov, avi, mkv, mp3, wav, flac, jpg, jpeg, png, bmp.
5. **Spusťte UI pro nastavení** (doporučeno pro první spuštění):
   ```bash
   python3 main.py
   ```
6. (Volitelné) **Spusťte bez GUI** – vhodné pro kiosk/reklamní obrazovku:
   ```bash
   python3 main.py --headless
   ```

> Tip: Pokud chcete, aby se přehrávač spustil po startu Raspberry Pi, můžete přidat příkaz `python3 /cesta/k/main.py --headless` do `~/.config/autostart/` (Desktop) nebo do systemd služby (Lite). Krátký návod je níže.

## Jak to funguje
- Konfigurace se ukládá do `config.json` (v kořeni projektu).
- `settings_ui.py` poskytuje jednoduché okno s volbou složky, autoplay, shuffle, hlasitost a zpoždění mezi položkami.
- `media_player.py` pomocí `python-vlc` načte playlist a přehrává jej ve smyčce. Umí náhodné pořadí a udržuje hlasitost.
- `main.py` je vstupní bod: buď spustí GUI (výchozí), nebo headless režim.

## Ovládání (GUI)
1. **Cílová složka** – vyberte, kde máte média.
2. **Autoplay při startu** – pokud je zaškrtnuto, přehrávání se spustí hned po otevření aplikace.
3. **Náhodné pořadí** – zamíchá playlist po každém uložení.
4. **Hlasitost** – rozsah 0–100.
5. **Zpoždění mezi položkami** – pauza mezi soubory (sekundy).
6. **Tlačítka**:
   - `Uložit nastavení` uloží do `config.json` a obnoví playlist.
   - `Zastavit` zastaví přehrávání.
   - `Spustit/Obnovit` znovu načte playlist a pustí přehrávání.

## Headless / kiosk režim
Pro čistý kioskový zážitek můžete skrýt kurzor a spustit přehrávač v plné obrazovce s VLC. Jednoduchý způsob přes systemd:

```bash
# Vytvořte službu
sudo tee /etc/systemd/system/rgb-loop.service <<'SERVICE'
[Unit]
Description=RGB Loop Media Player
After=network.target

[Service]
WorkingDirectory=/home/pi/MediaPlayer_raspberrypi
ExecStart=/usr/bin/python3 /home/pi/MediaPlayer_raspberrypi/main.py --headless
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
SERVICE

# Aktivujte
sudo systemctl daemon-reload
sudo systemctl enable rgb-loop.service
sudo systemctl start rgb-loop.service
```

## Struktura projektu
- `main.py` – vstupní bod, volba GUI vs headless.
- `settings_ui.py` – jednoduché Tkinter UI pro studenty.
- `media_player.py` – logika přehrávače a smyčky.
- `config.py` – načítání/ukládání `config.json`.
- `requirements.txt` – seznam Python závislostí.

## Tipy pro řešení problémů
- **Bez zvuku?** Zkontrolujte, zda je `vlc` správně nainstalované a audio výstup nastavený v Raspberry Pi OS.
- **Nejde spustit GUI?** Ujistěte se, že máte `python3-tk` (`sudo apt install python3-tk`).
- **Playlist je prázdný?** Ověřte přípony souborů a cestu k médiím v nastavení.

## Licence
MIT – můžete volně použít a upravit pro školní projekty.
