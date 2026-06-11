"""Generate 90 days of synthetic EV charging session data - with intentional dirt."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
rows = []
start = datetime(2026, 3, 1)
session_id = 100000

for day in range(90):
    date = start + timedelta(days=day)
    # weekly seasonality: weekends are ~25% quieter
    base = 1100 if date.weekday() < 5 else 825
    n_sessions = int(np.random.normal(base, 90))

    for _ in range(n_sessions):
        session_id += 1
        kwh = round(max(np.random.normal(18, 7), 1.5), 2)
        rows.append({
            "session_id": session_id,
            "session_date": date.strftime("%Y-%m-%d"),
            "charger_id": f"CK-{np.random.randint(1, 451):04d}",
            "city": np.random.choice(["London", "Manchester", "Bristol", "Glasgow"],
                                     p=[0.45, 0.25, 0.18, 0.12]),
            "kwh_delivered": kwh,
            "revenue_gbp": round(kwh * np.random.uniform(0.42, 0.55), 2),
            "charger_status": np.random.choice(["completed", "failed", "interrupted"],
                                               p=[0.91, 0.05, 0.04]),
        })

df = pd.DataFrame(rows)

# --- inject realistic data quality problems (your migration, recreated) ---
dirty = df.copy()
dupes = dirty.sample(150, random_state=1)                     # duplicate session IDs
dirty = pd.concat([dirty, dupes])
dirty.loc[dirty.sample(300, random_state=2).index, "kwh_delivered"] = np.nan   # nulls
dirty.loc[dirty.sample(80, random_state=3).index, "revenue_gbp"] *= -1         # negative revenue
future_idx = dirty.sample(40, random_state=4).index
dirty.loc[future_idx, "session_date"] = "2027-01-15"          # future dates
dirty.loc[dirty.sample(60, random_state=5).index, "charger_status"] = "UNKNOWN_STATE"

# simulate a migration outage: one day loses 70% of its volume
outage_day = "2026-04-18"
outage_rows = dirty[dirty.session_date == outage_day]
dirty = dirty.drop(outage_rows.sample(frac=0.7, random_state=6).index)

dirty.to_csv("ev_sessions_raw.csv", index=False)
print(f"Wrote{len(dirty):,} rows to ev_sessions_raw.csv - including hidden problems. Go find them.")