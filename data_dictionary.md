# Data Dictionary — Personal Stability Tracking

This project tracks daily subjective stability and contextual behavioural inputs.

One row = **one day**.

Apple Watch / Health data will be used separately for objective measures such as sleep and movement. This manual dataset focuses on **subjective stability ratings** and **context variables** that may influence stability.

---

# Core principles

- **Record once per day**, ideally at the same time (for example around 9pm).
- Use the **same rating anchors consistently** so scores remain comparable across weeks and months.
- Missing values should be avoided for the five stability anchors.

---

# Stability anchors

These five variables form the core stability measurement.

Each is rated from **0–10**.

## clarity (0–10)
How clear, grounded, and coherent your thinking felt.

Anchors:
- 0 → extremely scattered / racing / confused
- 5 → functional but somewhat foggy
- 10 → very clear, grounded, and coherent

---

## calm (0–10)
How emotionally steady you felt.

Anchors:

- 0 → highly agitated / anxious / irritable
- 5 → noticeable tension but manageable
- 10 → calm and emotionally steady most of the day

---

## routine (0–10)
How well daily structure held together.

Anchors:

- 0 → routine collapsed
- 5 → partial routine
- 10 → routine held well

Routine refers to things such as:

- meals
- hygiene
- movement
- key tasks
- general daily structure

---

## focus (0–10)
Ability to direct and sustain attention.

Anchors:

- 0 → extremely distracted / unable to concentrate
- 5 → moderate focus but inconsistent
- 10 → focused and mentally present

---

## resilience (0–10)
Ability to remain steady when encountering stress.

Anchors:

- 0 → easily thrown off by stressors
- 5 → some wobble but recovery possible
- 10 → remained steady under pressure

---

# Derived variable

## stability (0–10)
Overall stability score.

Definition:

```
stability = (clarity + calm + routine + focus + resilience) / 5
```

Round to **1 decimal place**.

---

# Context variables

These variables represent potential drivers of stability.

## coffee_cups (0–5)
Number of cups of coffee consumed during the day.

Examples:

- 0 → none
- 1 → one coffee
- 2 → two coffees
- etc.

The goal is **consistency**, not perfect caffeine measurement.

---

## social_hours (0–24)
Total hours spent in social interaction.

This may include:

- in‑person conversation
- phone or video calls
- meaningful online interaction

Decimals are allowed.

Examples:

- 0.5
- 1
- 2.75

---

## stressors (0–3)
Objective external stressor burden.

Anchors:

- 0 → none
- 1 → mild
- 2 → moderate
- 3 → heavy

Important:

This should reflect **external events**, not internal feelings.

Examples:

- administrative tasks
- conflict
- travel disruption
- work pressure

Internal anxiety alone should be reflected in the **calm** or **resilience** scores instead.

---

# Notes

## notes
Free text field for brief context.

Guidelines:

- Keep notes short
- Prefer factual context
- Useful for unusual events or explanations

Examples:

- "Good day overall, social evening"
- "High coffee, distracted"
- "Stressful admin tasks"

---

# Table schema

| Column | Type | Allowed | Meaning |
|------|------|------|------|
| date | string | YYYY‑MM‑DD | Day of record |
| clarity | float | 0–10 | Mental clarity |
| calm | float | 0–10 | Emotional steadiness |
| routine | float | 0–10 | Routine adherence |
| focus | float | 0–10 | Attention / presence |
| resilience | float | 0–10 | Ability to remain steady under stress |
| stability | float | 0–10 | Average of the five anchors |
| coffee_cups | int | 0–5 | Cups of coffee consumed |
| social_hours | float | 0–24 | Hours spent socially |
| stressors | int | 0–3 | External stressor burden |
| notes | string | free text | Context or anomalies |

---

# Data integrity rules

- `date` must be unique (one row per day)
- `stability` must equal the average of the five anchor variables
- `coffee_cups`, `social_hours`, and `stressors` must not be negative
- `stressors` should reflect objective events only

---

# Relationship to Apple Watch / Health data

Objective variables such as:

- sleep duration
- sleep stages
- steps
- heart rate
- activity

will be imported separately from Apple Health exports.

These can later be merged with the stability dataset using the **date** column.

Keeping these systems separate ensures:

- fast daily logging
- clearer measurement design
- better long‑term data quality

---

# Example row

```csv
date,clarity,calm,routine,focus,resilience,stability,coffee_cups,social_hours,stressors,notes
2026-02-25,7,6,8,7,6,6.8,2,1.5,1,"Pretty steady overall, mild stress"
```