CREATE TABLE IF NOT EXISTS data_forge_admin.pipeline_run_audit (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    trigger_source TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'running',
    details JSONB NOT NULL DEFAULT '{}'::JSONB
);

CREATE TABLE IF NOT EXISTS data_forge_admin.schema_change_notes (
    version_rank INTEGER NOT NULL,
    installed_rank INTEGER NOT NULL,
    migration_type TEXT NOT NULL,
    migration_description TEXT NOT NULL,
    reviewed_by TEXT,
    reviewed_at TIMESTAMPTZ,
    notes TEXT,
    PRIMARY KEY (installed_rank)
);
