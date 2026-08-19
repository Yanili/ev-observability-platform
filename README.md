# EV Charging Data Observability Platform

**Catches data quality failures and metric anomalies at the source — before they reach a dashboard or a stakeholder.**

An 8-week self-directed build documenting a transition from BI/reporting analyst to analytics engineer: Python → Spark/Delta → dbt → CI/CD → BI reporting.

---

## The problem

A platform migration let data quality issues slip through unnoticed until stakeholders stopped trusting the numbers. By the time a broken metric surfaces on a dashboard, the damage is already done — the fix is reactive, and the trust is hard to win back.

This project moves that check **upstream**. It validates data and flags anomalies at the pipeline level, so failures are caught and blocked before they ever reach a report.

## The approach

A layered pipeline that ingests raw EV charging sessions, aggregates them into daily metrics, monitors day-over-day variance, flags anomalies, and enforces data quality rules as automated tests gated by CI — every change is checked before it can merge.

## Architecture

```
raw sessions (CSV)
      │
      ▼
Python DQ engine ──── 6 automated rules, critical/warning severity
      │
      ▼
Spark + Delta ─────── historical snapshots, incremental load, MA7 + variance
      │
      ▼
dbt (3-layer) ─────── staging → intermediate → marts
      │               + 10+ tests (generic / custom / relationships)
      ▼
GitHub Actions ────── dbt build runs on every PR; blocks merge on regression
      │
      ▼
Power BI  (in progress) ── freshness / quality / business metrics / anomalies
```

## Tech stack

Python · PySpark · Delta Lake · **dbt Core** · GitHub Actions (CI/CD) · Git · Power BI

*(dbt models are warehouse-agnostic standard SQL; the BI layer is the final phase in progress.)*

---

## Engineering highlights

**Data quality engine — 6 automated rules.**
Duplicates, future dates, negative revenue, invalid status values, and null critical fields, each tagged critical or warning. Critical failures halt the pipeline; warnings surface without blocking.

**Anomaly detection that beats naive checks.**
Uses 7-day moving averages and window functions rather than simple row-count checks — which let it catch a simulated 70% outage day that a row-count check would have missed entirely.

**Historical snapshot pipeline.**
Spark + Delta with incremental loading and day-over-day variance / trend monitoring, partitioned by day.

**3-layer dbt architecture, fully documented.**
- **Staging** — `stg_ev_sessions`: cleaned session-level data from raw source.
- **Intermediate** — `int_daily_metrics` (per-charger daily aggregation) and `int_variance_metrics` (day-over-day variance via `LAG`).
- **Marts** — `fct_observability`: consumption-ready table with variance %, anomaly flags, and new-charger detection; `anomaly_detection`: surfaces only anomalous charger-days for alerting.
- Every model and column documented in `.yml`; full lineage graph via `dbt docs`.

**Test suite — 10+ tests with severity tiers.**
Generic (`not_null`, `unique`, `accepted_values`, `relationships`), plus custom singular tests (`no_future_dates`, `no_negative_revenue`, `no_negative_energy`, `assert_no_anomalies`). A `dim_chargers` seed acts as a charger master reference for foreign-key validation — and deliberately excludes a few charger IDs present in the session data to simulate an unregistered-asset scenario, demonstrating the `relationships` test catching orphan records.

**CI/CD with GitHub Actions.**
Every pull request runs `dbt build` via GitHub Actions. Branch protection blocks merges when data quality tests fail, and failures notify by email.

---

## Two decisions worth reading

These are the judgement calls the project is really about — not the tools, but knowing what to do when the naive setup misfires.

### Baselining known data quality issues

The source dataset contains pre-existing defects (148 duplicates, 778 orphan sessions, 40 future-dated rows, 1 invalid status). Setting these tests to `error` meant *every* pull request was blocked — including changes unrelated to data quality, such as documentation updates.

Rather than deleting the defects (which removes the demonstration value) or downgrading the tests to `warn` (which removes the protection), the tests use baseline thresholds via `error_if`. Counts at or below the known baseline warn; anything above it errors and blocks the merge. **The pipeline blocks *regressions*, not *history*.**

*Known refinement:* thresholds are currently absolute counts derived from the initial dataset. A future iteration would use proportional thresholds (e.g. `dbt_utils.not_null_proportion`) so they stay meaningful as data volume grows.

### Anomaly threshold tuning

The anomaly flag was initially set at a 50% day-over-day variance threshold. On first run this flagged ~55% of all charger-days as anomalous — effectively alert fatigue, where everything is flagged and nothing is actionable. EV charging demand fluctuates heavily day-to-day, so a 50% swing is normal, not exceptional.

After analysing the variance distribution across thresholds (50% / 100% / 200% / 500%), the threshold was tightened to 500%, bringing the anomaly rate down to ~3% of charger-days — a level where flagged events genuinely warrant investigation. The threshold is parameterised as a dbt variable (`anomaly_threshold` in `dbt_project.yml`) rather than hardcoded, so it can be tuned per environment without editing model SQL.

*Known refinement:* a fixed percentage threshold is a heuristic. A future iteration could use statistical baselining (e.g. flagging deviations beyond N standard deviations) to adapt per-charger rather than applying one global cutoff.

---

## What's next

- **Power BI reporting layer** — four pages: data freshness, data quality, business metrics, anomalies.

---

<details>
<summary><strong>Weekly progress log</strong> (the 8-week build, day by day)</summary>

### Week 0 — Setup
Environment set up, repo created.

### Week 1 — Python as a data engineering foundation
- Day 1: Python lists as time-series; found the weekend dip pattern.
- Day 2: dict = one fact-table row; built computed snapshot metrics.
- Day 3: reusable functions as testable measures.
- Day 4: migration forensics — caught 5 planted data quality bugs with pandas.
- Day 5: moving-average anomaly detection; volume monitoring beats row checks.
- Day 6: aggregated raw EV sessions into daily metrics, computed 7-day moving averages, flagged volume anomalies — caught a simulated 70% outage day.

### Week 2 — Spark fundamentals
- Day 1: Spark DataFrames; schema inference risk after migration.
- Day 2: lazy evaluation; transformations vs actions.
- Day 3: groupBy in Spark; why segment-level monitoring matters.
- Day 4: window functions as testable time intelligence.
- Day 5: Delta time travel; incremental vs full refresh.
- Weekend: historical snapshot pipeline — Spark + Delta, partitioned daily metrics with MA7 and variance, incremental loading.

### Week 3 — Data quality engineering
- Day 1–2: DQ rules 1–5 — duplicates, future dates, negative revenue, status whitelist, null criticals; all planted bugs caught.
- Day 3: DQ runner — loop rules into a list, `spark.createDataFrame`, timestamped results to Delta.
- Day 4: critical vs warning labels; raise exception to stop the pipeline.
- Day 5: custom rule from real migration experience — `check_positive_kwh`.
- Weekend: DQ engine — 6 automated rules with critical/warning severity, results persisted to Delta.

### Week 4 — Git & going public
- Day 1: Git branches — created first feature branch, merged locally.
- Day 2: pull requests — pushed branch to GitHub, opened and merged first PR.
- Day 3: merge conflicts — created and resolved a conflict in VS Code, learned `merge --abort`.
- Day 4: `.gitignore` audit before going public — fixed `__pycache__` typo, removed a tracked `.pyc` with `git rm --cached`.
- Day 5: README v2 — portfolio landing page; repo made public.

### Weeks 5–7 — dbt, testing, CI/CD
- Week 5: 3-layer dbt architecture (staging → intermediate → marts), variance and anomaly models, threshold tuning.
- Week 6: full test suite — generic + custom + relationships tests, severity tiers, `dim_chargers` seed.
- Week 7: GitHub Actions CI/CD — `dbt build` on every PR, branch protection, baseline thresholds.

</details>
