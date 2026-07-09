--models\intermediate\int_variance_metrics.sql

with daily as (
    select * from {{ref('int_daily_metrics')}}
),

 _previous as (
    select 
        charger_id,
        metric_date,
        total_kwh_delivered,
        total_sessions,
        total_revenue,
        lag(total_kwh_delivered) over (partition by charger_id order by metric_date) as prev_total_kwh_delivered,
        lag(total_sessions) over (partition by charger_id order by metric_date) as prev_total_sessions,
        lag(total_revenue) over (partition by charger_id order by metric_date) as prev_total_revenue
    from daily
)

select
    charger_id,
    metric_date,
    total_kwh_delivered,
    prev_total_kwh_delivered,
    total_kwh_delivered - prev_total_kwh_delivered as variance_kwh_delivered,
    case when prev_total_kwh_delivered is null then 'new charger' else 'need_to_check' end as kwh_delivered_status,
    total_sessions,
    prev_total_sessions,
    total_sessions - prev_total_sessions as variance_sessions,
    case when prev_total_sessions is null then 'new charger' else 'need_to_check' end as sessions_status,
    total_revenue,
    prev_total_revenue,
    total_revenue - prev_total_revenue as variance_revenue,
    case when prev_total_revenue is null then 'new charger' else 'need_to_check' end as revenue_status
from _previous
