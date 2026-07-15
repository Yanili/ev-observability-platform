-- models/marts/anomaly_detection.sql
-- Surfaces ONLY the charger-days where a metric is anomalous
-- One row = one anomalous event, for alering / investigation 

with observability as (
    select 
        *
    from {{ ref('fct_observability') }}
)

select charger_id,
metric_date,kwh_delivered_variance_pct,revenue_variance_pct,sessions_variance_pct
from observability
where kwh_is_anomaly = 'yes' or revenue_is_anomaly = 'yes' or sessions_is_anomaly = 'yes'
