# Raw Data Directory

This folder contains **real personal habit tracking data**.

⚠️ This data is private and excluded from version control via `.gitignore`.

---

## Purpose

The `raw/` directory stores the original, manually recorded dataset before any cleaning, validation, or transformation.

Files in this folder are:

- Untouched
- Unmodified
- The source of truth
- Logged exactly as recorded each day

No derived variables or engineered features should exist here.

---

## Main File

### Expected file

`habits.csv`

This file:

- Contains **one row per day**
- Uses the column structure defined in `data_dictionary.md`
- Is appended daily (never rewritten wholesale)
- Should not contain duplicate dates

---

## Required Schema

The file must follow the structure defined in `data_dictionary.md`.

Required columns:

- date
- clarity
- calm
- routine
- focus
- resilience
- stability
- coffee_cups
- social_hours
- stressors
- notes

Column definitions, allowed ranges, and rating anchors are specified in `data_dictionary.md`. The schema reflects the five stability anchors plus contextual variables (coffee intake, social time, and objective stressors).

---

## Update Process

Daily workflow:

1. Run the logger script:  
   `python scripts/log_today.py`
2. Enter the five stability anchors
3. Enter coffee cups, social hours, and objective stressors
4. Optionally add notes
5. The script automatically appends the new row to `habits.csv`

---

## Data Integrity Rules

- Do not retroactively edit past rows unless correcting a clear logging mistake.
- Do not change historical ratings to “smooth” data.
- Do not remove rows unless a duplicate exists.
- Dates must be unique (one entry per day).
- Stability should equal `(clarity + calm + routine + focus + resilience) / 5`.

---

## Privacy & Security

This dataset contains personal behavioural and mental-state data.

This folder must never be committed to GitHub.

Your `.gitignore` should include:

- `data/raw/*`
- `!data/raw/README.md`

Verify with:

`git status`

`habits.csv` should not appear as staged or untracked.

---

## Data Lifecycle

Raw → Processed → Analysis

1. Raw data lives in `data/raw/`
2. Validation and cleaning may produce outputs in `data/processed/`
3. Notebooks should read from processed data where possible
4. Raw data remains unchanged

---

## Philosophy

This folder represents the highest-fidelity record of daily behavioural input.

Accuracy and consistency are more important than perfection.
Missing values are acceptable.
Fabricated precision is not.