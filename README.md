# Idle Cult Empire Save Editor

A small Python script that edits the local save files of the Android game
**Idle Cult Empire** (`com.wa.cult.empire.tycoon.idle.game`). The game stores its
save as plain JSON `*.slot` files, so no special tools are needed.

> For single-player use only. Not affiliated with the game's developer.
> Editing saves can corrupt your progress, so **always keep a backup**.
> Use at your own risk.

## What it does

| File | Change |
|---|---|
| `Trade.slot` | Sets the premium currency (`Hard`) |
| `Location_City.slot` | Sets all resources (Wood, Stone, Board, BonesBlock, Potion, Potion2, SoulCrystal, SoulCrystal2, Book, MagicScrolls, Lamp, Wax, EvilHoney, Mushroom, Mushroom2), Matter and Faith. Optionally unlocks all islands |
| `Ads.slot` | Turns on `BypassInterstitial` and `BypassRewarded` |

## Requirements

- Python 3.7+ (no extra packages)

## Usage

1. **Close the game completely** (swipe it away from recent apps).
2. Copy the game's `*.slot` files to a folder (see *Finding your save files*).
3. Run:

```bash
python3 idle_editor.py /path/to/slot_folder
```

Options:

| Option | Default | Meaning |
|---|---|---|
| `--hard N` | `999999` | Premium currency amount |
| `--resource N` | `1e9` | Amount for each resource |
| `--islands` | off | Also unlock all locked islands (may skip story progression) |

Example:

```bash
python3 idle_editor.py ./slots --islands --hard 500000 --resource 5e8
```

4. Copy the edited files back to the game's folder and start the game.

A `.bak` copy of every file is made the first time it is edited. Re-running never
overwrites that backup. To undo everything, rename the `.bak` files back.

## Finding your save files

- **Rooted:** `/data/data/com.wa.cult.empire.tycoon.idle.game/files/`
- **Unrooted:** try `Android/data/com.wa.cult.empire.tycoon.idle.game/files/`
  on internal storage (Android 11+ restricts this folder; a file manager with
  Shizuku support can access it).

Look for files ending in `.slot`.

## Running on the phone (Termux)

```bash
pkg install python
python3 idle_editor.py /sdcard/slots
```

## Troubleshooting

- **A file is skipped:** the script prints "not found" and continues. `Ads.slot`
  only appears after the game has been running for a while.
- **Premium currency resets to 0:** the game keeps a `HardHistory` log in
  `Trade.slot`. If a plain edit is rejected, the log may need to match the new
  balance.
- **Ads still show:** the bypass flags may be ignored. Blocking ads with Private
  DNS (`dns.adguard-dns.com`) is a fallback.
- **Resources don't show up:** resource names are inferred from the game's own
  keys and may not all be used. Open an issue with the file attached.
- **Game crashes or resets the save:** restore the `.bak` files.

## Disclaimer

Provided as is, without warranty. Do not use it in any online or competitive
mode.
