-- tests/no_negative_energy.sql 
-- Business rule: energy cannot be negative
-- This test returns rows that violate the rule. 0 rows = pass

Select session_id, kwh_delivered
from {{ref('stg_ev_sessions')}}
where kwh_delivered < 0