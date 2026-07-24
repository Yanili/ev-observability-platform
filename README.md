Yani's project
An 8-week build: from BI analyst to analytics engineer.
Detects data quality failures and metric anomalies in EV charging data — before they reach stakeholders
# EV Charging Data Observability Platform


## Project statement
A platform migration left data quality issue slipping through unnoticed until stakeholders stopped trusting the numbers This project catches those failures and metric anomalies at the source, before they even reach a dashboard.

## Architecture sketch 
raw csv -> Spark/Data -> DQ rules -> (coming : dbt -> CI/CD -> Power BI)

## What's built so far 
**DQ engine** - 6 automated rules (duplicates, future dates, negative revenue, invalid status,null criticals) with critical/warning severity that blocks the pipeline on critical failures 
**Anomaly detection** - using 7-day moving averages and window functions - caught a simulated 70% outage day that simple row-count checks missed 
**Historical snapshot pipeline** - Spark + Delta, with incremental loading and variance/trend monitoring
**dbt project** : 3-layer model architecture (staging -> intermediate -> fact) with full documentation and lineage.
- Staging: 'stg_ev_sessions' - cleaned session-level data from raw source
- Intermediate: 'int_daily_metrics' (pre charger aggregation), 'int_variance_matrics(day-over-day variance via LAG)
- Fact: fct_observability' - consumption-ready tabel with variance%,anomaly flags(>50% absolute change) and new-charger detection
- Every model and column documented via '.yml' descriptions; full linage graph generated with 'dbt docs'
**dbt test suite**: 10+ tests(generic + custom + relationships) catching every planned migration bug, with severity tiers
Generic@ 'no null','unique','accepted_value','relationship'
Custom (signualr) : 'no_future_dates','no_negative_revenue','no_negative_energy','assert_no_anomalies'
Seed: 'dim_chargers' as a charger master referene for foreign-key validation 

### Baselining known data quality issues
The source dataset contains pre-existing defects (148 duplicates, 778 orphan
sessions, 40 future-dated rows, 1 invalid status). Setting these tests to
error meant every pull request was blocked — including changes unrelated to
data quality, such as documentation updates.
Rather than deleting the defects (which would remove the demonstration value)
or downgrading the tests to warn (which would remove the protection), the
tests now use baseline thresholds via error_if. Counts at or below the known
baseline warn; anything above it errors and blocks the merge. The pipeline
therefore blocks *regressions* rather than *history*.
*Known refinement:* thresholds are currently absolute counts derived from the
initial dataset. A future iteration would use proportional thresholds (e.g.
dbt_utils.not_null_proportion) so they remain meaningful as data volume grows.### Baselining known data quality issue

**CI/CD pipeline**: (.github\workflows\dbt_ci.yml)
every pull request runs'dbt build' against Snowflake via GitHub Actions.
CI verification
CI failures notify via GitHub email 
Add branch protection with active mode
## Coming next:
Power BI reporting
Noted : dim_chargers deliberately excludes a small number of charger_id
present in session data, simulating an unregistered-asset scenario
This demonstrates the relationships test catching orphan records

## Teach stack
Python, PySpark, Delta Lake, (dbt,Snowflake,GitHub Actions - coming)

## Progress Log
Week 0: environment set up, repo created
Day 1: Python list as time-series; found the weekend dip pattern
Day 2 : dict = one fact-table row; build computed snapshot metrics
Day 3 : resuable functions = testable dax mesaure
Day 4 : migration forensics - caught 5 planted data quality bugs with pandas
Day 5 : moving-average anomaly detection; volume monitoring beats row checks
Day 6 : aggregates raw ev charging sessions into daily metrics, computes 7-day moving aerages,flags volume anomalies catches a simulated 70% outage day


Week 2 : Spark Fundamentals
day 1 : Spark DataFrames;schema inference risk after migraion
day 2 : lazy evalutaion;transformations vs actions
day 3 : groupBy in Spark;wht segment-level monitoring matters
day 4 : window functions = dax time intelligence, but testable
day 5 : Delta time travel;incremental vs full refresh
Weekend : What's built so far" : Historical Snapshot Pipeline
        Spark + Delta, partitioned daily metrics with MA7 and variance, incremental loading

Week 3 : Data Quailty Engineering
Day 1 & 2 : DQ rules 1-5 - duplicates, future dates, negative revenue, status whitelist and null criticals;all planted bugs caught
Day 3 : DQ runner; loop rules into list;spark.createdataframe;timestamped results to Delta
Day 4 : critical vs warning label; rasie exception to stop pipeline
Day 5 : custom rule from real migration experience - [check_positive_kwh]
Weekend : ** Data Engine** (week3/): 6 automated rules with critical/warning severity, results persisted to Delta

Week 4 
Day 1 : it branches - created first feature branch, merged lgocally
Day 2 : Pull request - pushed branch to GitHub, opened and mergerd first PR
Day 3 : Merge conflicts - created and resolved a conflict in VS code, learned merge -- abort
Day 4 : gitignore aduit before going public - fixed __pycache__typo, remove a tracked .pyc with git rm-cached 
Day 5 : README v2 - portfolio landing page (problem statment, architecture sketch,teach stack);repo made public 


### Anomaly threshold tuning
The anomaly flag was initially set at a 50% day-over-day variance threshold.
On first run this flagged ~55% of all charger-days as anomalous — effectively
alert fatigue, where everything is flagged and nothing is actionable. EV charging
demand fluctuates heavily day-to-day, so a 50% swing is normal, not exceptional.
After analysing the variance distribution across thresholds (50% / 100% / 200% /
500%), the threshold was tightened to 500%, bringing the anomaly rate down to ~3%
of charger-days — a level where flagged events genuinely warrant investigation.
The threshold is parameterised as a dbt variable (anomaly_threshold in
dbt_project.yml) rather than hardcoded, so it can be adjusted per environment
or stakeholder without editing model SQL.
*Known refinement:* a fixed percentage threshold is a heuristic. A future
iteration could use statistical baselining (e.g. flagging deviations beyond N
standard deviations) to adapt per-charger rather than applying one global cutoff.
