# ev-observability-platform
Yani's project
# EV Charging Data Observability Platform

An 8-week build: from BI analyst to analytics engineer.
Detects data quality failures and metric anomalies in EV charging
data — before they reach stakeholders.

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