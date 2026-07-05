Yani's project
An 8-week build: from BI analyst to analytics engineer.
Detects data quality failures and metric anomalies in EV charging data — before they reach stakeholders
# EV Charging Data Observability Platform


## Project statement
A platform migration left data quality issue slipping through unnoticed until stakeholders stopped trusting the numbers This project catches those failures and metric anomalies at the source, before they even reach a dashboard.

## Architecture sketch 
raw csv -> Spark/Data -> DQ rules -> (coming : dbt -> CI/CD -> Power BI)

## What's built so far 
DQ engine - 6 automated rules (duplicates, future dates, negative revenue, invalid status,null criticals) with critical/warning severity that blocks the pipeline on critical failures 
Anomaly detection - using 7-day moving averages and window functions - caught a simulated 70% outage day that simple row-count checks missed 
Historical snapshot pipeline - Spark + Delta, with incremental loading and variance/trend monitoring
Coming next: dbt models+tests on Snowflake, CI/CD via GitHub Actions, Power BI reporting

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

Week 4 Day1 : it branches - created first feature branch, merged lgocally

How DQ engineering works , 6 rules for session, energy, reveune, date etc, 5 critical and 1 warning label
result will be saved in dq summary

Day 2 : Pull request - pushed branch to GitHub, opened and mergerd first PR
How DQ engineering works , 6 rules for session, energy, reveune, date etc, 5 critical and 1 warning label ->  result will be saved and showed in dq summary

Day3 : Merge conflicts - created and resolved a conflict in VS code, learned merge -- abort


