-- test/no_future_dates.sql
-- Business rule: a session cannot start in the future
-- This test returns rowa that vidlate the rule. 0 rows = pass

select session_id, session_date
from {{ref('stg_ev_sessions')}}
where session_date > current_date()