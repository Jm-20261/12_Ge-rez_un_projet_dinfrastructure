CREATE TABLE IF NOT EXISTS reward_parameters (
    parameter_name TEXT PRIMARY KEY,
    parameter_value NUMERIC NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS commute_checks (
    employee_id TEXT,
    employee_name TEXT,
    home_address TEXT,
    company_address TEXT,
    commute_mode TEXT,
    distance_km NUMERIC,
    max_allowed_km NUMERIC,
    validation_status TEXT,
    validation_comment TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sport_activities (
    activity_id TEXT PRIMARY KEY,
    employee_id TEXT NOT NULL,
    activity_start TIMESTAMP NOT NULL,
    activity_end TIMESTAMP,
    activity_type TEXT NOT NULL,
    distance_m NUMERIC,
    elapsed_time_s NUMERIC,
    comment TEXT,
    source TEXT DEFAULT 'simulation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reward_results (
    employee_id TEXT NOT NULL,
    employee_name TEXT,
    salary_annual_gross NUMERIC,
    commute_mode TEXT,
    validation_status TEXT,
    commute_eligible BOOLEAN,
    sports_activity_count INTEGER,
    wellbeing_days_eligible BOOLEAN,
    wellbeing_days_awarded INTEGER,
    prime_rate NUMERIC,
    prime_amount NUMERIC,
    estimated_total_cost NUMERIC,
    year_ref INTEGER,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    step_name TEXT NOT NULL,
    status TEXT NOT NULL,
    rows_processed INTEGER,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
