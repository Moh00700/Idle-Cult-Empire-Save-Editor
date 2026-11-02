#!/usr/bin/env python3
"""
Save editor for com.wa.cult.empire.tycoon.idle.game (the *.slot JSON files).

Usage:
  python3 idle_editor.py <slot_folder> [--hard N] [--resource N] [--islands]

Close the game first. A .bak copy of each file is made the first time it is
changed (re-running never overwrites your original backup).
"""
import argparse, json, re, shutil
from pathlib import Path


def backup(p: Path):
    b = p.with_name(p.name + ".bak")
    if not b.exists():
        shutil.copy2(p, b)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--hard", type=float, default=999_999, help="premium currency (default 999999)")
    ap.add_argument("--resource", type=float, default=1e9, help="amount of each resource (default 1e9)")
    ap.add_argument("--islands", action="store_true", help="also unlock all locked islands")
    args = ap.parse_args()
    folder = Path(args.folder)

    trade = folder / "Trade.slot"
    if trade.exists():
        backup(trade)
        d = json.loads(trade.read_text())
        d["$"]["Hard"] = args.hard
        trade.write_text(json.dumps(d, indent=2))
        print(f"Trade.slot: Hard = {args.hard:g}")
    else:
        print("Trade.slot not found, skipped")

    city = folder / "Location_City.slot"
    if city.exists():
        backup(city)
        d = json.loads(city.read_text())
        mp = d["ModuleParams"]
        names = {"Wood", "Stone", "Matter"}
        for v in mp.values():
            for k in v:
                m = re.match(r"Production_Tycoon_(\w+)", k)
                if m:
                    names.add(m.group(1))
        root = mp["Root"]
        for n in names:
            root[n] = args.resource
        root["Matter"] = 1e6
        root["Faith"] = 100000.0
        print(f"Location_City.slot: {len(names)} resources = {args.resource:g}")
        if args.islands:
            n = 0
            for k, v in mp.items():
                if "Island" in k and v.get("Level") == 0.0:
                    v["Level"] = 1.0
                    n += 1
            print(f"Location_City.slot: opened {n} islands")
        city.write_text(json.dumps(d, indent=2))
    else:
        print("Location_City.slot not found, skipped")

    ads = folder / "Ads.slot"
    if ads.exists():
        backup(ads)
        d = json.loads(ads.read_text())
        d["BypassRewarded"] = True
        d["BypassInterstitial"] = True
        ads.write_text(json.dumps(d, indent=2))
        print("Ads.slot: ad bypass flags on")
    else:
        print("Ads.slot not found, skipped (it appears after the game has run a while)")


if __name__ == "__main__":
    main()
