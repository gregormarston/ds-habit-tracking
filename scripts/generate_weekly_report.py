import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "habits.csv"
REPORTS_PATH = PROJECT_ROOT / "reports"

REPORTS_PATH.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Last 7 days
end_date = df["date"].max()
start_date = end_date - timedelta(days=6)
weekly = df[df["date"] >= start_date]

if len(weekly) < 3:
    print("Not enough data for weekly report.")
    exit()

# Metrics
mean_stability = weekly["stability"].mean()
mean_sleep = weekly["sleep_hours"].mean()
total_social = weekly["social_minutes"].sum()
high_stress_days = (weekly["stressors"] >= 2).sum()

best_day = weekly.loc[weekly["stability"].idxmax()]
worst_day = weekly.loc[weekly["stability"].idxmin()]

# Correlations
corr_sleep = weekly["sleep_hours"].corr(weekly["stability"])
corr_stress = weekly["stressors"].corr(weekly["stability"])

# Plot
plt.figure()
plt.plot(weekly["date"], weekly["stability"])
plt.title("Weekly Stability Trend")
plt.xticks(rotation=45)
plt.tight_layout()

chart_path = REPORTS_PATH / f"weekly_{end_date.date()}.png"
plt.savefig(chart_path)
plt.close()

# Markdown report
report_path = REPORTS_PATH / f"weekly_{end_date.date()}.md"

with open(report_path, "w") as f:
    f.write(f"# Weekly Stability Report ({start_date.date()} → {end_date.date()})\n\n")
    f.write(f"Mean Stability: {mean_stability:.2f}\n\n")
    f.write(f"Mean Sleep: {mean_sleep:.2f} hours\n\n")
    f.write(f"Total Social Minutes: {total_social}\n\n")
    f.write(f"High Stress Days: {high_stress_days}\n\n")
    f.write(f"Best Day: {best_day['date'].date()} ({best_day['stability']:.1f})\n\n")
    f.write(f"Worst Day: {worst_day['date'].date()} ({worst_day['stability']:.1f})\n\n")
    f.write(f"Correlation Sleep vs Stability: {corr_sleep:.2f}\n\n")
    f.write(f"Correlation Stress vs Stability: {corr_stress:.2f}\n\n")
    f.write(f"![Weekly Chart]({chart_path.name})\n")

print(f"Weekly report generated: {report_path}")