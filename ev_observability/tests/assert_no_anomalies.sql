-- tests/assert_no_anomalies.sql
-- Fails if ANY anomaly exists. Each row in anomaly_detection is an anomaly,
-- so simply selecting from it = the failing rows.

{{config(
    severity='warn'
)}}

select * from {{ref('anomaly_detection') }}