--models\intermediate\int_daily_metrics.sql

with session as (
    select * from {{ref('stg_ev_sessions')}}
),

daily as (
    select 
    CHARGER_ID,
    date_trunc('day', SESSION_DATE) as METRIC_DATE,
    sum(KWH_DELIVERED) as TOTAL_KWH_DELIVERED,
    count(distinct SESSION_ID) as TOTAL_SESSIONS,
    sum(REVENUE_GBP) as TOTAL_REVENUE
    from session
    group by charger_id, date_trunc('day', SESSION_DATE)
)

select * from daily