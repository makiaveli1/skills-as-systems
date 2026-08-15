CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('queued', 'leased', 'done', 'cancelled')),
    lease_owner TEXT,
    lease_until INTEGER,
    result TEXT
);

CREATE INDEX IF NOT EXISTS jobs_ready
ON jobs(state, lease_until, id);

CREATE TABLE IF NOT EXISTS deliveries (
    job_id TEXT PRIMARY KEY REFERENCES jobs(id),
    worker TEXT NOT NULL,
    delivered_at INTEGER NOT NULL,
    result TEXT NOT NULL
);

PRAGMA user_version = 1;
