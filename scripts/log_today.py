#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import date as dt_date
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "habits.csv"

FIELDNAMES = [
    "date",
    "clarity",
    "calm",
    "routine",
    "focus",
    "resilience",
    "stability",
    "coffee_cups",
    "social_hours",
    "stressors",
    "notes",
]

RANGES = {
    "clarity": (0.0, 10.0),
    "calm": (0.0, 10.0),
    "routine": (0.0, 10.0),
    "focus": (0.0, 10.0),
    "resilience": (0.0, 10.0),
    "stability": (0.0, 10.0),
    "coffee_cups": (0.0, 5.0),
    "social_hours": (0.0, 24.0),
    "stressors": (0.0, 3.0),
}

INT_FIELDS = {
    "coffee_cups",
    "stressors",
}


def compute_stability(
    clarity: float,
    calm: float,
    routine: float,
    focus: float,
    resilience: float,
) -> float:
    return round((clarity + calm + routine + focus + resilience) / 5.0, 1)


def prompt_str(msg: str, default: Optional[str] = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        val = input(f"{msg}{suffix}: ").strip()
        if val == "" and default is not None:
            return default
        if val != "" or default == "":
            return val


def prompt_number(field: str, msg: str, default: Optional[str] = None) -> float:
    lo, hi = RANGES[field]
    while True:
        raw = prompt_str(msg, default=default)
        try:
            x = float(raw)
        except ValueError:
            print(f"  ✖ Please enter a number (got '{raw}').")
            continue

        if x < lo or x > hi:
            print(f"  ✖ Out of range for {field}: {lo}–{hi} (got {x}).")
            continue

        if field in INT_FIELDS and not float(x).is_integer():
            print(f"  ✖ {field} must be an integer (got {x}).")
            continue

        return x


def existing_dates(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return set()
        return {row.get("date", "").strip() for row in reader if row.get("date")}


def ensure_csv_header(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()


def main() -> int:
    today_default = dt_date.today().isoformat()

    print("\nDaily Stability Logger")
    print(f"Writing to: {CSV_PATH}")
    print("Press Enter to accept defaults.\n")

    ensure_csv_header(CSV_PATH)

    date_str = prompt_str("Date (YYYY-MM-DD)", default=today_default)
    dates = existing_dates(CSV_PATH)
    if date_str in dates:
        print(f"\n✖ An entry for {date_str} already exists in habits.csv.")
        print("  If you need to fix it, edit the CSV manually.")
        return 1

    print("\nRate the five stability anchors:")
    clarity = prompt_number(
        "clarity",
        "Clarity (0–10; racing/scattered → grounded/clear)"
    )
    calm = prompt_number(
        "calm",
        "Calm (0–10; mood swings/irritability → calm/steady)"
    )
    routine = prompt_number(
        "routine",
        "Routine (0–10; structure collapsed → routine held well)"
    )
    focus = prompt_number(
        "focus",
        "Focus (0–10; very distracted → focused/present)"
    )
    resilience = prompt_number(
        "resilience",
        "Resilience (0–10; easily thrown off → steady under stress)"
    )

    stability = compute_stability(clarity, calm, routine, focus, resilience)
    print(f"Computed stability: {stability:.1f}\n")

    coffee_cups = prompt_number(
        "coffee_cups",
        "Coffee cups (0–5)",
        default="0",
    )
    social_hours = prompt_number(
        "social_hours",
        "Social hours (0–24; decimals allowed)",
        default="0",
    )
    stressors = prompt_number(
        "stressors",
        "Objective stressors (0–3)",
        default="0",
    )

    notes = prompt_str("Notes (short; commas OK)", default="")

    row = {
        "date": date_str,
        "clarity": f"{clarity:.0f}" if clarity.is_integer() else f"{clarity}",
        "calm": f"{calm:.0f}" if calm.is_integer() else f"{calm}",
        "routine": f"{routine:.0f}" if routine.is_integer() else f"{routine}",
        "focus": f"{focus:.0f}" if focus.is_integer() else f"{focus}",
        "resilience": f"{resilience:.0f}" if resilience.is_integer() else f"{resilience}",
        "stability": f"{stability:.1f}",
        "coffee_cups": f"{int(coffee_cups)}",
        "social_hours": f"{social_hours}".rstrip("0").rstrip(".") if social_hours % 1 else f"{social_hours:.1f}".rstrip("0").rstrip("."),
        "stressors": f"{int(stressors)}",
        "notes": notes,
    }

    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)

    print(f"\n✅ Logged {date_str} successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
