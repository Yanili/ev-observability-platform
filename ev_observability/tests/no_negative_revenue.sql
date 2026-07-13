-- tests/no_negative_revenue.sql
-- Business rule: revenue cannot be negative
-- This test returns rows that violate the rule. 0 rows = pass

select session_id, revenue_gbp
from {{ref('stg_ev_sessions')}}
where revenue_gbp < 0