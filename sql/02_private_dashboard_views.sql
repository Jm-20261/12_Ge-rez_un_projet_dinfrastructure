CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT
    (SELECT COUNT(*) FROM employees) AS total_employees,
    (SELECT COUNT(*) FROM sport_activities) AS total_activities,
    (SELECT COUNT(*) FROM reward_results WHERE commute_eligible = TRUE) AS employees_prime_eligible,
    (SELECT COUNT(*) FROM reward_results WHERE wellbeing_days_eligible = TRUE) AS employees_wellbeing_eligible,
    (SELECT COALESCE(SUM(wellbeing_days_awarded), 0) FROM reward_results) AS total_wellbeing_days_awarded,
    (SELECT COALESCE(SUM(prime_amount), 0) FROM reward_results) AS total_prime_cost;

CREATE OR REPLACE VIEW vw_activities_by_month AS
SELECT
    DATE_TRUNC('month', activity_start) AS activity_month,
    activity_type,
    COUNT(*) AS activity_count,
    COALESCE(SUM(distance_m), 0) AS total_distance_m
FROM sport_activities
GROUP BY 1, 2
ORDER BY 1, 2;

CREATE OR REPLACE VIEW vw_top_sports AS
SELECT
    activity_type,
    COUNT(*) AS activity_count,
    COALESCE(SUM(distance_m), 0) AS total_distance_m
FROM sport_activities
GROUP BY activity_type
ORDER BY activity_count DESC;

CREATE OR REPLACE VIEW vw_commute_status AS
SELECT
    commute_mode,
    validation_status,
    COUNT(*) AS employee_count
FROM commute_checks
GROUP BY commute_mode, validation_status
ORDER BY commute_mode, validation_status;

CREATE OR REPLACE VIEW vw_employee_rewards AS
SELECT
    rr.employee_id,
    rr.employee_name,
    rr.salary_annual_gross,
    rr.commute_mode,
    rr.validation_status,
    rr.commute_eligible,
    rr.sports_activity_count,
    rr.wellbeing_days_eligible,
    rr.wellbeing_days_awarded,
    rr.prime_rate,
    rr.prime_amount,
    rr.estimated_total_cost,
    rr.year_ref
FROM reward_results rr
ORDER BY rr.prime_amount DESC, rr.employee_name;
