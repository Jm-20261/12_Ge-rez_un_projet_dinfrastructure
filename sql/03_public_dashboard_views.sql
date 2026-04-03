CREATE OR REPLACE VIEW vw_public_kpi_summary AS
SELECT
    (SELECT COUNT(*) FROM employees) AS total_employees,
    (SELECT COUNT(*) FROM employee_sports WHERE has_declared_sport = TRUE) AS sporting_employees,
    (SELECT COUNT(*) FROM sport_activities) AS total_activities,
    (SELECT COUNT(*) FROM reward_results WHERE commute_eligible = TRUE) AS commute_eligible_employees,
    (SELECT COUNT(*) FROM reward_results WHERE wellbeing_days_eligible = TRUE) AS wellbeing_eligible_employees,
    ROUND(
        100.0 * (SELECT COUNT(*) FROM employee_sports WHERE has_declared_sport = TRUE)
        / NULLIF((SELECT COUNT(*) FROM employees), 0),
        1
    ) AS participation_rate_pct;

CREATE OR REPLACE VIEW vw_public_declared_sports AS
SELECT
    main_sport,
    COUNT(*) AS declared_employee_count
FROM employee_sports
WHERE has_declared_sport = TRUE
  AND main_sport IS NOT NULL
GROUP BY main_sport
ORDER BY declared_employee_count DESC;

CREATE OR REPLACE VIEW vw_public_activities_by_month AS
SELECT
    DATE_TRUNC('month', activity_start)::date AS activity_month,
    COUNT(*) AS activity_count
FROM sport_activities
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE VIEW vw_public_top_sports AS
SELECT
    activity_type,
    COUNT(*) AS activity_count
FROM sport_activities
GROUP BY activity_type
ORDER BY activity_count DESC;

CREATE OR REPLACE VIEW vw_public_commute_modes AS
SELECT
    commute_mode,
    COUNT(*) AS employee_count
FROM employees
GROUP BY commute_mode
ORDER BY employee_count DESC;
