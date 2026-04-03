CREATE OR REPLACE VIEW vw_pipeline_status AS
SELECT
    step_name,
    status,
    rows_processed,
    message,
    created_at
FROM pipeline_runs
ORDER BY created_at DESC;

CREATE OR REPLACE VIEW vw_quality_summary AS
SELECT
    status,
    COUNT(*) AS check_count
FROM quality_checks_results
GROUP BY status
ORDER BY status;

CREATE OR REPLACE VIEW vw_latest_table_volumes AS
SELECT DISTINCT ON (table_name)
    table_name,
    row_count,
    measured_at
FROM table_volume_history
ORDER BY table_name, measured_at DESC;

CREATE OR REPLACE VIEW vw_table_volume_history AS
SELECT
    table_name,
    row_count,
    measured_at
FROM table_volume_history
ORDER BY measured_at DESC, table_name;

DROP VIEW IF EXISTS vw_monitoring_last_success;

CREATE VIEW vw_monitoring_last_success AS
SELECT
    TO_CHAR(
        (MAX(created_at) AT TIME ZONE 'UTC') AT TIME ZONE 'Europe/Paris',
        'DD/MM/YYYY HH24:MI:SS'
    ) AS last_successful_run_at
FROM pipeline_runs
WHERE status = 'SUCCESS';

CREATE OR REPLACE VIEW vw_monitoring_failed_steps AS
SELECT
    COUNT(*) AS failed_steps_count
FROM pipeline_runs
WHERE status = 'FAILED';

CREATE OR REPLACE VIEW vw_monitoring_failed_quality_checks AS
SELECT
    COUNT(*) AS failed_quality_checks_count
FROM quality_checks_results
WHERE status = 'FAIL';

CREATE TABLE IF NOT EXISTS kpi_history (
    snapshot_id SERIAL PRIMARY KEY,
    snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_employees INTEGER,
    total_activities INTEGER,
    employees_prime_eligible INTEGER,
    employees_wellbeing_eligible INTEGER,
    total_wellbeing_days_awarded INTEGER,
    total_prime_cost NUMERIC
);

CREATE OR REPLACE VIEW vw_latest_kpi_snapshot AS
SELECT *
FROM kpi_history
ORDER BY snapshot_at DESC
LIMIT 1;

CREATE OR REPLACE VIEW vw_kpi_history AS
SELECT
    snapshot_at,
    total_employees,
    total_activities,
    employees_prime_eligible,
    employees_wellbeing_eligible,
    total_wellbeing_days_awarded,
    total_prime_cost
FROM kpi_history
ORDER BY snapshot_at DESC;