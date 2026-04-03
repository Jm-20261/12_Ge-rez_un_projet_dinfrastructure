DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_analytics') THEN
        CREATE ROLE role_analytics LOGIN PASSWORD 'analytics123';
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_rh_admin') THEN
        CREATE ROLE role_rh_admin LOGIN PASSWORD 'rhadmin123';
    END IF;
END
$$;

ALTER ROLE role_analytics WITH PASSWORD 'analytics123';
ALTER ROLE role_rh_admin WITH PASSWORD 'rhadmin123';

GRANT CONNECT ON DATABASE sport_data TO role_analytics;
GRANT CONNECT ON DATABASE sport_data TO role_rh_admin;

GRANT USAGE ON SCHEMA public TO role_analytics;
GRANT USAGE ON SCHEMA public TO role_rh_admin;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM role_analytics;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM role_analytics;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM role_rh_admin;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM role_rh_admin;

GRANT SELECT ON TABLE
    vw_public_kpi_summary,
    vw_public_declared_sports,
    vw_public_activities_by_month,
    vw_public_top_sports,
    vw_public_commute_modes
TO role_analytics;

GRANT SELECT ON TABLE
    vw_kpi_summary,
    vw_activities_by_month,
    vw_top_sports,
    vw_commute_status,
    vw_employee_rewards,
    vw_pipeline_status,
    vw_quality_summary,
    vw_latest_table_volumes,
    vw_table_volume_history,
    vw_monitoring_last_success,
    vw_monitoring_failed_steps,
    vw_monitoring_failed_quality_checks,
    vw_latest_kpi_snapshot,
    vw_kpi_history
TO role_rh_admin;
