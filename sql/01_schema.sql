CREATE TABLE IF NOT EXISTS rh_raw (
    id_salarie TEXT,
    nom TEXT,
    prenom TEXT,
    date_de_naissance TIMESTAMP,
    bu TEXT,
    date_d_embauche TIMESTAMP,
    salaire_brut NUMERIC,
    type_de_contrat TEXT,
    nombre_de_jours_de_cp NUMERIC,
    adresse_du_domicile TEXT,
    moyen_de_deplacement TEXT
);

CREATE TABLE IF NOT EXISTS sport_raw (
    id_salarie TEXT,
    pratique_d_un_sport TEXT
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    full_name TEXT,
    home_address TEXT,
    commute_mode TEXT,
    salary_annual_gross NUMERIC,
    bu TEXT,
    hire_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS employee_sports (
    employee_sport_id SERIAL PRIMARY KEY,
    employee_id TEXT,
    main_sport TEXT,
    has_declared_sport BOOLEAN,
    source TEXT
);

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

CREATE TABLE IF NOT EXISTS quality_checks_results (
    check_id SERIAL PRIMARY KEY,
    check_name TEXT,
    table_name TEXT,
    failed_rows INTEGER,
    status TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    step_name TEXT NOT NULL,
    status TEXT NOT NULL,
    rows_processed INTEGER,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS table_volume_history (
    metric_id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);