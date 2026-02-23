from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


REQUIRED_COLUMNS = [
    "date",
    "clarity",
    "calm",
    "routine",
    "stability",
    "sleep_hours",
    "sleep_quality",
    "exercise_minutes",
    "caffeine_units",
    "social_minutes",
    "stressors",
    "notes",
]

RANGES = {
    "clarity": (0.0, 10.0),
    "calm": (0.0, 10.0),
    "routine": (0.0, 10.0),
    "stability": (0.0, 10.0),
    "sleep_hours": (0.0, 16.0),
    "sleep_quality": (1.0, 5.0),
    "exercise_minutes": (0.0, 300.0),
    "caffeine_units": (0.0, 20.0),
    "social_minutes": (0.0, 1440.0),
    "stressors": (0.0, 3.0),
}

INT_FIELDS = {
    "sleep_quality",
    "exercise_minutes",
    "caffeine_units",
    "social_minutes",
    "stressors",
}

FLOAT_FIELDS = {
    "clarity",
    "calm",
    "routine",
    "stability",
    "sleep_hours",
}


@dataclass
class Issue:
    row_number: int
    column: str
    message: str


def _is_blank(value: Optional[str]) -> bool:
    return value is None or value.strip() == ""


def _to_float(value: str) -> Optional[float]:
    if _is_blank(value):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _validate_columns(header: List[str]) -> List[str]:
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    extras = [c for c in header if c not in REQUIRED_COLUMNS]
    messages: List[str] = []
    if missing:
        messages.append(f"Missing columns: {missing}")
    if extras:
        messages.append(f"Unexpected extra columns: {extras}")
    return messages


def compute_stability(clarity: float, calm: float, routine: float) -> float:
    return round((clarity + calm + routine) / 3.0, 1)


def validate_csv(path: Path, write_back: bool = False) -> Tuple[List[Issue], int]:
    issues: List[Issue] = []
    rows_out: List[Dict[str, str]] = []

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [Issue(0, "", "CSV has no header row")], 0

        header = reader.fieldnames
        header_issues = _validate_columns(header)
        for msg in header_issues:
            issues.append(Issue(0, "header", msg))

        seen_dates = set()
        valid_rows = 0

        for idx, row in enumerate(reader, start=2):  # 1=header, so data starts at line 2
            # Keep original row for potential write-back
            row_clean = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

            # Date checks
            date = row_clean.get("date", "")
            if _is_blank(date):
                issues.append(Issue(idx, "date", "Missing date"))
            else:
                if date in seen_dates:
                    issues.append(Issue(idx, "date", f"Duplicate date: {date}"))
                seen_dates.add(date)

            # Type + range checks
            numeric_values: Dict[str, Optional[float]] = {}
            for col in RANGES.keys():
                val = row_clean.get(col, "")
                if _is_blank(val):
                    numeric_values[col] = None
                    continue

                fval = _to_float(val)
                if fval is None:
                    issues.append(Issue(idx, col, f"Not a number: '{val}'"))
                    numeric_values[col] = None
                    continue

                lo, hi = RANGES[col]
                if fval < lo or fval > hi:
                    issues.append(Issue(idx, col, f"Out of range {lo}–{hi}: {fval}"))
                numeric_values[col] = fval

                # int-only fields should be integer-like
                if col in INT_FIELDS and not float(fval).is_integer():
                    issues.append(Issue(idx, col, f"Expected integer, got: {fval}"))

            # Compute stability if possible
            clarity = numeric_values.get("clarity")
            calm = numeric_values.get("calm")
            routine = numeric_values.get("routine")

            if clarity is not None and calm is not None and routine is not None:
                computed = compute_stability(clarity, calm, routine)
                existing = numeric_values.get("stability")

                if existing is None:
                    # fill missing stability
                    row_clean["stability"] = f"{computed:.1f}"
                else:
                    # allow small rounding differences
                    if abs(existing - computed) > 0.1:
                        issues.append(
                            Issue(
                                idx,
                                "stability",
                                f"Does not match (clarity+calm+routine)/3. "
                                f"Existing={existing:.1f}, Computed={computed:.1f}",
                            )
                        )

            rows_out.append(row_clean)
            valid_rows += 1

    if write_back:
        # Write back with the required column order (stable & reproducible)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
            writer.writeheader()
            for r in rows_out:
                # ensure all required keys exist
                out_row = {c: r.get(c, "") for c in REQUIRED_COLUMNS}
                writer.writerow(out_row)

    return issues, valid_rows


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_and_compute_stability.py <path-to-csv> [--write]")
        print("Example: python scripts/validate_and_compute_stability.py data/raw/habits.csv --write")
        return 2

    csv_path = Path(sys.argv[1]).expanduser()
    write_back = "--write" in sys.argv[2:]

    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 2

    issues, row_count = validate_csv(csv_path, write_back=write_back)

    print(f"Checked: {csv_path}")
    print(f"Rows: {row_count}")

    if not issues:
        print("✅ No issues found.")
        if write_back:
            print("✅ Wrote back computed stability values (if any were missing).")
        return 0

    print(f"⚠️ Issues: {len(issues)}")
    for issue in issues:
        if issue.row_number == 0:
            print(f"[HEADER] {issue.message}")
        else:
            print(f"[Line {issue.row_number}] {issue.column}: {issue.message}")

    # Non-zero exit if issues exist (useful later for CI)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())