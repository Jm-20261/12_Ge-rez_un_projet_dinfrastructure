-- =========================================================
-- Nettoyage léger avant ajout des contraintes
-- =========================================================

UPDATE employee_sports
SET has_declared_sport = FALSE
WHERE has_declared_sport IS NULL;

UPDATE employees
SET is_active = TRUE
WHERE is_active IS NULL;

UPDATE reward_results
SET sports_activity_count = COALESCE(sports_activity_count, 0),
    wellbeing_days_awarded = COALESCE(wellbeing_days_awarded, 0),
    prime_rate = COALESCE(prime_rate, 0),
    prime_amount = COALESCE(prime_amount, 0),
    estimated_total_cost = COALESCE(estimated_total_cost, 0)
WHERE sports_activity_count IS NULL
   OR wellbeing_days_awarded IS NULL
   OR prime_rate IS NULL
   OR prime_amount IS NULL
   OR estimated_total_cost IS NULL;

UPDATE quality_checks_results
SET failed_rows = COALESCE(failed_rows, 0)
WHERE failed_rows IS NULL;

UPDATE table_volume_history
SET row_count = COALESCE(row_count, 0)
WHERE row_count IS NULL;

UPDATE kpi_history
SET total_employees = COALESCE(total_employees, 0),
    total_activities = COALESCE(total_activities, 0),
    employees_prime_eligible = COALESCE(employees_prime_eligible, 0),
    employees_wellbeing_eligible = COALESCE(employees_wellbeing_eligible, 0),
    total_wellbeing_days_awarded = COALESCE(total_wellbeing_days_awarded, 0),
    total_prime_cost = COALESCE(total_prime_cost, 0)
WHERE total_employees IS NULL
   OR total_activities IS NULL
   OR employees_prime_eligible IS NULL
   OR employees_wellbeing_eligible IS NULL
   OR total_wellbeing_days_awarded IS NULL
   OR total_prime_cost IS NULL;

-- =========================================================
-- employees
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'employees_salary_non_negative_chk'
    ) THEN
        ALTER TABLE employees
        ADD CONSTRAINT employees_salary_non_negative_chk
        CHECK (salary_annual_gross IS NULL OR salary_annual_gross >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'employees_commute_mode_allowed_chk'
    ) THEN
        ALTER TABLE employees
        ADD CONSTRAINT employees_commute_mode_allowed_chk
        CHECK (
            commute_mode IS NULL
            OR commute_mode IN (
                'Marche/Running',
                'Transports en commun',
                'Véhicule',
                'Vélo/Trottinette/Autres'
            )
        );
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'employees_full_name_not_blank_chk'
    ) THEN
        ALTER TABLE employees
        ADD CONSTRAINT employees_full_name_not_blank_chk
        CHECK (full_name IS NULL OR BTRIM(full_name) <> '');
    END IF;
END $$;

-- =========================================================
-- employee_sports
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'employee_sports_has_declared_not_null_chk'
    ) THEN
        ALTER TABLE employee_sports
        ADD CONSTRAINT employee_sports_has_declared_not_null_chk
        CHECK (has_declared_sport IS NOT NULL);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'employee_sports_employee_fk'
    ) THEN
        ALTER TABLE employee_sports
        ADD CONSTRAINT employee_sports_employee_fk
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id);
    END IF;
END $$;

-- =========================================================
-- reward_parameters
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_parameters_value_non_negative_chk'
    ) THEN
        ALTER TABLE reward_parameters
        ADD CONSTRAINT reward_parameters_value_non_negative_chk
        CHECK (parameter_value >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_parameters_name_not_blank_chk'
    ) THEN
        ALTER TABLE reward_parameters
        ADD CONSTRAINT reward_parameters_name_not_blank_chk
        CHECK (BTRIM(parameter_name) <> '');
    END IF;
END $$;

-- =========================================================
-- commute_checks
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'commute_checks_distance_non_negative_chk'
    ) THEN
        ALTER TABLE commute_checks
        ADD CONSTRAINT commute_checks_distance_non_negative_chk
        CHECK (distance_km IS NULL OR distance_km >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'commute_checks_max_allowed_non_negative_chk'
    ) THEN
        ALTER TABLE commute_checks
        ADD CONSTRAINT commute_checks_max_allowed_non_negative_chk
        CHECK (max_allowed_km IS NULL OR max_allowed_km >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'commute_checks_validation_status_allowed_chk'
    ) THEN
        ALTER TABLE commute_checks
        ADD CONSTRAINT commute_checks_validation_status_allowed_chk
        CHECK (
            validation_status IS NULL
            OR validation_status IN (
                'VALID',
                'TO_REVIEW',
                'ERROR',
                'NOT_APPLICABLE',
                'PENDING_API_KEY'
            )
        );
    END IF;
END $$;

-- =========================================================
-- sport_activities
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'sport_activities_employee_fk'
    ) THEN
        ALTER TABLE sport_activities
        ADD CONSTRAINT sport_activities_employee_fk
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'sport_activities_distance_non_negative_chk'
    ) THEN
        ALTER TABLE sport_activities
        ADD CONSTRAINT sport_activities_distance_non_negative_chk
        CHECK (distance_m IS NULL OR distance_m >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'sport_activities_elapsed_non_negative_chk'
    ) THEN
        ALTER TABLE sport_activities
        ADD CONSTRAINT sport_activities_elapsed_non_negative_chk
        CHECK (elapsed_time_s IS NULL OR elapsed_time_s >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'sport_activities_dates_consistent_chk'
    ) THEN
        ALTER TABLE sport_activities
        ADD CONSTRAINT sport_activities_dates_consistent_chk
        CHECK (activity_end IS NULL OR activity_end >= activity_start);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'sport_activities_type_not_blank_chk'
    ) THEN
        ALTER TABLE sport_activities
        ADD CONSTRAINT sport_activities_type_not_blank_chk
        CHECK (BTRIM(activity_type) <> '');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'sport_activities_source_not_blank_chk'
    ) THEN
        ALTER TABLE sport_activities
        ADD CONSTRAINT sport_activities_source_not_blank_chk
        CHECK (source IS NULL OR BTRIM(source) <> '');
    END IF;
END $$;

-- =========================================================
-- reward_results
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_employee_unique_uk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_employee_unique_uk
        UNIQUE (employee_id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_salary_non_negative_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_salary_non_negative_chk
        CHECK (salary_annual_gross IS NULL OR salary_annual_gross >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_activity_count_non_negative_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_activity_count_non_negative_chk
        CHECK (sports_activity_count IS NULL OR sports_activity_count >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_wellbeing_days_allowed_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_wellbeing_days_allowed_chk
        CHECK (wellbeing_days_awarded IN (0, 5));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_prime_rate_range_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_prime_rate_range_chk
        CHECK (prime_rate IS NULL OR (prime_rate >= 0 AND prime_rate <= 1));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_prime_amount_non_negative_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_prime_amount_non_negative_chk
        CHECK (prime_amount IS NULL OR prime_amount >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_total_cost_non_negative_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_total_cost_non_negative_chk
        CHECK (estimated_total_cost IS NULL OR estimated_total_cost >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_validation_status_allowed_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_validation_status_allowed_chk
        CHECK (
            validation_status IS NULL
            OR validation_status IN (
                'VALID',
                'TO_REVIEW',
                'ERROR',
                'NOT_APPLICABLE',
                'PENDING_API_KEY'
            )
        );
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'reward_results_year_ref_range_chk'
    ) THEN
        ALTER TABLE reward_results
        ADD CONSTRAINT reward_results_year_ref_range_chk
        CHECK (year_ref IS NULL OR year_ref BETWEEN 2020 AND 2100);
    END IF;
END $$;

-- =========================================================
-- quality_checks_results
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'quality_checks_failed_rows_non_negative_chk'
    ) THEN
        ALTER TABLE quality_checks_results
        ADD CONSTRAINT quality_checks_failed_rows_non_negative_chk
        CHECK (failed_rows >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'quality_checks_status_allowed_chk'
    ) THEN
        ALTER TABLE quality_checks_results
        ADD CONSTRAINT quality_checks_status_allowed_chk
        CHECK (status IN ('PASS', 'FAIL'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'quality_checks_name_not_blank_chk'
    ) THEN
        ALTER TABLE quality_checks_results
        ADD CONSTRAINT quality_checks_name_not_blank_chk
        CHECK (check_name IS NULL OR BTRIM(check_name) <> '');
    END IF;
END $$;

-- =========================================================
-- pipeline_runs
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'pipeline_runs_status_allowed_chk'
    ) THEN
        ALTER TABLE pipeline_runs
        ADD CONSTRAINT pipeline_runs_status_allowed_chk
        CHECK (status IN ('SUCCESS', 'FAILED'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'pipeline_runs_rows_processed_non_negative_chk'
    ) THEN
        ALTER TABLE pipeline_runs
        ADD CONSTRAINT pipeline_runs_rows_processed_non_negative_chk
        CHECK (rows_processed IS NULL OR rows_processed >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'pipeline_runs_step_name_not_blank_chk'
    ) THEN
        ALTER TABLE pipeline_runs
        ADD CONSTRAINT pipeline_runs_step_name_not_blank_chk
        CHECK (BTRIM(step_name) <> '');
    END IF;
END $$;

-- =========================================================
-- table_volume_history
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'table_volume_history_row_count_non_negative_chk'
    ) THEN
        ALTER TABLE table_volume_history
        ADD CONSTRAINT table_volume_history_row_count_non_negative_chk
        CHECK (row_count >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'table_volume_history_table_name_not_blank_chk'
    ) THEN
        ALTER TABLE table_volume_history
        ADD CONSTRAINT table_volume_history_table_name_not_blank_chk
        CHECK (BTRIM(table_name) <> '');
    END IF;
END $$;

-- =========================================================
-- kpi_history
-- =========================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'kpi_history_total_employees_non_negative_chk'
    ) THEN
        ALTER TABLE kpi_history
        ADD CONSTRAINT kpi_history_total_employees_non_negative_chk
        CHECK (total_employees >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'kpi_history_total_activities_non_negative_chk'
    ) THEN
        ALTER TABLE kpi_history
        ADD CONSTRAINT kpi_history_total_activities_non_negative_chk
        CHECK (total_activities >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'kpi_history_prime_eligible_non_negative_chk'
    ) THEN
        ALTER TABLE kpi_history
        ADD CONSTRAINT kpi_history_prime_eligible_non_negative_chk
        CHECK (employees_prime_eligible >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'kpi_history_wellbeing_eligible_non_negative_chk'
    ) THEN
        ALTER TABLE kpi_history
        ADD CONSTRAINT kpi_history_wellbeing_eligible_non_negative_chk
        CHECK (employees_wellbeing_eligible >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'kpi_history_wellbeing_days_non_negative_chk'
    ) THEN
        ALTER TABLE kpi_history
        ADD CONSTRAINT kpi_history_wellbeing_days_non_negative_chk
        CHECK (total_wellbeing_days_awarded >= 0);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'kpi_history_total_prime_cost_non_negative_chk'
    ) THEN
        ALTER TABLE kpi_history
        ADD CONSTRAINT kpi_history_total_prime_cost_non_negative_chk
        CHECK (total_prime_cost >= 0);
    END IF;
END $$;
