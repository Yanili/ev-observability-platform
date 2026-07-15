--models\marts\fct_observability.sql
with variance as (
    select * from {{ref('int_variance_metrics')}}
),

_var_pct as (
    select charger_id, 
    metric_date,
    total_kwh_delivered,
    prev_total_kwh_delivered,
    variance_kwh_delivered,
    case when prev_total_kwh_delivered is null OR prev_total_kwh_delivered = 0 then NULL
    else ((total_kwh_delivered - prev_total_kwh_delivered) / prev_total_kwh_delivered)*100 end as kwh_delivered_variance_pct,
    total_sessions,
    prev_total_sessions,
    variance_sessions,
    case when prev_total_sessions is null OR prev_total_sessions = 0 then NULL
    else ((total_sessions - prev_total_sessions) / prev_total_sessions)*100 end as sessions_variance_pct,
    total_revenue, 
    prev_total_revenue,
    variance_revenue,
    case when prev_total_revenue is null OR prev_total_revenue = 0 then NULL
    else ((total_revenue - prev_total_revenue) / prev_total_revenue)*100 end as revenue_variance_pct
    from variance
)

select charger_id, 
metric_date,
total_kwh_delivered,
prev_total_kwh_delivered,
variance_kwh_delivered,
kwh_delivered_variance_pct,
case when kwh_delivered_variance_pct is null then 'no_baseline' 
else case when abs(kwh_delivered_variance_pct) > {{ var('anomaly_threshold') }} then 'yes' -- {{ var('anomaly_threshold') }} is a heuristic threshold, to be defined with statistical methods baselining
else 'no' end end as kwh_is_anomaly,
total_sessions,
prev_total_sessions,
variance_sessions,
sessions_variance_pct,
case when sessions_variance_pct is null then 'no_baseline' 
else case when abs(sessions_variance_pct) > {{ var('anomaly_threshold') }} then 'yes' -- {{ var('anomaly_threshold') }} is a heuristic threshold, to be defined with statistical methods baselining
else 'no' end end as sessions_is_anomaly,
total_revenue,
prev_total_revenue,
variance_revenue,
revenue_variance_pct,
case when revenue_variance_pct is null then 'no_baseline' 
else case when abs(revenue_variance_pct) > {{ var('anomaly_threshold') }} then 'yes' -- {{ var('anomaly_threshold') }} is a heuristic threshold, to be defined with statistical methods baselining
else 'no' end end as revenue_is_anomaly
from _var_pct