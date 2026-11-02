#!/usr/bin/env python3
"""
Save editor for com.wa.cult.empire.tycoon.idle.game (the *.slot JSON files).

Nothing is changed unless you ask for it: every edit is its own option.

Examples:
  python3 idle_editor.py slots --list
  python3 idle_editor.py slots --hard 999999
  python3 idle_editor.py slots --wood 1e9 --stone 5e8
  python3 idle_editor.py slots --all-resources 1e9
  python3 idle_editor.py slots --island PotionIsland --island LibraryIsland
  python3 idle_editor.py slots --all-islands
  python3 idle_editor.py slots --no-ads

Close the game first. A .bak copy of each file is made the first time it is
changed (re-running never overwrites your original backup).
"""
import argparse, json, shutil, sys
from pathlib import Path

RESOURCES = ["Wood", "Stone", "Board", "BonesBlock", "Potion", "Potion2",
             "SoulCrystal", "SoulCrystal2", "Book", "MagicScrolls", "Lamp",
             "Wax", "EvilHoney", "Mushroom", "Mushroom2"]
OTHER = ["Matter", "Faith"]  # also stored in Root, handled like resources


def backup(p: Path):
    b = p.with_name(p.name + ".bak")
    if not b.exists():
        shutil.copy2(p, b)


def load(p: Path):
    if not p.exists():
        print(f"{p.name} not found, skipped")
        return None
    return json.loads(p.read_text())


def save(p: Path, d):
    backup(p)
    p.write_text(json.dumps(d, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="folder containing the .slot files")
    ap.add_argument("--list", action="store_true", help="show current values and exit (changes nothing)")

    g = ap.add_argument_group("premium currency")
    g.add_argument("--hard", type=float, metavar="N", help="set premium currency (Trade.slot)")

    g = ap.add_argument_group("resources (Location_City.slot), each separate")
    for r in RESOURCES + OTHER:
        g.add_argument(f"--{r.lower()}", type=float, metavar="N", help=f"set {r}")
    g.add_argument("--all-resources", type=float, metavar="N", help="set every resource above to N")

    g = ap.add_argument_group("islands (Location_City.slot), separate from resources")
    g.add_argument("--island", action="append", default=[], metavar="NAME",
                   help="unlock one island by name (repeatable; use --list for names)")
    g.add_argument("--all-islands", action="store_true", help="unlock every locked island")

    g = ap.add_argument_group("ads")
    g.add_argument("--no-ads", action="store_true", help="turn on the ad-bypass flags (Ads.slot)")

    a = ap.parse_args()
    folder = Path(a.folder)
    trade, city, ads = folder / "Trade.slot", folder / "Location_City.slot", folder / "Ads.slot"

    # ---------------------------------------------------------------- list
    if a.list:
        t = load(trade)
        if t:
            print(f"Hard: {t['$'].get('Hard')}")
        c = load(city)
        if c:
            mp = c["ModuleParams"]
            root = mp["Root"]
            print("Resources:")
            for r in RESOURCES + OTHER:
                print(f"  {r}: {root.get(r, 0)}")
            print("Islands:")
            for k, v in mp.items():
                if "Island" in k:
                    print(f"  {k}: {'unlocked' if v.get('Level', 0) >= 1 else 'locked'}")
        d = load(ads)
        if d:
            print(f"Ads: BypassInterstitial={d.get('BypassInterstitial')} BypassRewarded={d.get('BypassRewarded')}")
        return

    res = {r: getattr(a, r.lower()) for r in RESOURCES + OTHER if getattr(a, r.lower()) is not None}
    if a.all_resources is not None:
        for r in RESOURCES + OTHER:
            res.setdefault(r, a.all_resources)
    islands_wanted = a.all_islands or a.island
    if not (a.hard is not None or res or islands_wanted or a.no_ads):
        ap.print_help()
        print("\nNothing to do: pick at least one option.")
        return

    # ---------------------------------------------------------------- hard
    if a.hard is not None:
        t = load(trade)
        if t:
            t["$"]["Hard"] = a.hard
            save(trade, t)
            print(f"Hard = {a.hard:g}")

    # ---------------------------------------------------------------- resources / islands
    if res or islands_wanted:
        c = load(city)
        if c:
            mp = c["ModuleParams"]
            for r, v in res.items():
                mp["Root"][r] = v
                print(f"{r} = {v:g}")
            if islands_wanted:
                islands = [k for k in mp if "Island" in k]
                if a.all_islands:
                    targets = [k for k in islands if mp[k].get("Level", 0) == 0]
                else:
                    targets = []
                    lower = {k.lower(): k for k in islands}
                    for name in a.island:
                        k = lower.get(name.lower())
                        if k is None:
                            print(f"Unknown island '{name}' (use --list to see names)")
                        else:
                            targets.append(k)
                for k in targets:
                    mp[k]["Level"] = 1.0
                    print(f"Island unlocked: {k}")
            save(city, c)

    # ---------------------------------------------------------------- ads
    if a.no_ads:
        d = load(ads)
        if d:
            d["BypassRewarded"] = True
            d["BypassInterstitial"] = True
            save(ads, d)
            print("Ad bypass flags on")


if __name__ == "__main__":
    main()
