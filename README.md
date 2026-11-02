# Idle Cult Empire Save Editor

A lightweight Python tool for editing local save files of **Idle Cult Empire**
(`com.wa.cult.empire.tycoon.idle.game`) on Android. Set currency, resources, unlock
islands and enable ad-bypass flags with a single command.

- No dependencies, only Python 3.7+
- Automatic backups before any change
- Every edit is optional and independent

> **Disclaimer:** For offline, single-player use only. Not affiliated with the
> game's developer. Provided as is. Always keep a backup of your save.

## Quick start

```bash
# 1. See your current values (changes nothing)
python3 idle_editor.py slots --list

# 2. Make your edits
python3 idle_editor.py slots --hard 999999 --all-resources 1e9 --no-ads
```

`slots` is the folder containing your copied `.slot` files. See
[Getting your save files](#getting-your-save-files).

## Options

Nothing is changed unless you pass an option. Options can be combined.

| Option | Description |
|---|---|
| `--list` | Show current values and exit |
| `--hard N` | Set the premium currency |
| `--all-resources N` | Set every resource to `N` |
| `--wood N`, `--stone N`, ... | Set a single resource (see below) |
| `--island NAME` | Unlock one island (repeatable) |
| `--all-islands` | Unlock every locked island |
| `--no-ads` | Enable the ad-bypass flags |

**Resources:** `wood`, `stone`, `board`, `bonesblock`, `potion`, `potion2`,
`soulcrystal`, `soulcrystal2`, `book`, `magicscrolls`, `lamp`, `wax`, `evilhoney`,
`mushroom`, `mushroom2`, `matter`, `faith`.

**Islands:** names are case-insensitive. Run `--list` to see them all.

### Examples

```bash
python3 idle_editor.py slots --wood 1e9 --stone 5e8
python3 idle_editor.py slots --island PotionIsland --island LibraryIsland
python3 idle_editor.py slots --all-islands
```

## Getting your save files

The tool uses up to three files from the game's data folder:

| File | Used for |
|---|---|
| `Trade.slot` | Premium currency |
| `Location_City.slot` | Resources and islands |
| `Ads.slot` | Ad-bypass flags (appears after the game has run for a while) |

Missing files are skipped.

**Location**

- Rooted: `/data/data/com.wa.cult.empire.tycoon.idle.game/files/`
- Unrooted: `Android/data/com.wa.cult.empire.tycoon.idle.game/files/` on internal
  storage (Android 11+ restricts this folder; use a file manager with Shizuku access)

## Workflow

1. Close the game completely.
2. Copy the `.slot` files into a folder.
3. Run the tool with the options you want.
4. Copy the edited files back, replacing the originals.
5. Start the game.

Running on the phone with [Termux](https://termux.dev):

```bash
pkg install python
python3 idle_editor.py /sdcard/slots --all-resources 1e9
```

## Backups and undo

The first time a file is changed, a copy is saved next to it as `<name>.slot.bak`.
Re-running never overwrites that backup. To undo, rename the `.bak` files back.

## Troubleshooting

| Problem | Fix |
|---|---|
| "file not found, skipped" | Check the folder path. `Ads.slot` only exists after the game has run a while |
| Premium currency resets to 0 | The game keeps a history log in `Trade.slot`. A plain edit may be rejected |
| Ads still show | The flags may be ignored. Private DNS (`dns.adguard-dns.com`) is a fallback |
| A resource doesn't change | Not every resource may be used by the game. Open an issue with the file attached |
| Game crashes or resets the save | Restore the `.bak` files |

## License

MIT, see [LICENSE](LICENSE).
