-- ev_observability/tests/deliberate_failure.sql
--
-- INTENTIONAL FAILURE - FOR CI DEMONSTRATION ONLY
--
-- This test has no WHERE clause, so it will always return rows and always fails. 
-- Purpose: prove that the CI pipeline can detect a failing test and blocks the merge.
-- This file is never merged into main - the PR is closed after the red check is captured.

select session_id 
from {{ ref('stg_session') }}
limit 10