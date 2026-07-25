CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TYPE account_role AS ENUM ('owner', 'admin', 'member', 'viewer');
CREATE TYPE holding_source AS ENUM ('manual', 'csv', 'broker_oauth', 'mock');
CREATE TYPE alert_severity AS ENUM ('info', 'warning', 'critical');

CREATE TABLE IF NOT EXISTS app_user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS workspace (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES app_user(id),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS workspace_member (
    workspace_id UUID NOT NULL REFERENCES workspace(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
    role account_role NOT NULL DEFAULT 'member',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (workspace_id, user_id)
);

CREATE TABLE IF NOT EXISTS portfolio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspace(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    base_currency CHAR(3) NOT NULL DEFAULT 'INR',
    source holding_source NOT NULL,
    broker_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS instrument (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    isin TEXT,
    name TEXT NOT NULL,
    asset_class TEXT NOT NULL,
    sector TEXT,
    UNIQUE (exchange, symbol)
);

CREATE TABLE IF NOT EXISTS position (
    portfolio_id UUID NOT NULL REFERENCES portfolio(id) ON DELETE CASCADE,
    instrument_id UUID NOT NULL REFERENCES instrument(id),
    quantity NUMERIC(20, 6) NOT NULL CHECK (quantity >= 0),
    average_cost NUMERIC(20, 6) NOT NULL CHECK (average_cost >= 0),
    as_of TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (portfolio_id, instrument_id)
);

CREATE TABLE IF NOT EXISTS price_bar (
    instrument_id UUID NOT NULL REFERENCES instrument(id),
    observed_at TIMESTAMPTZ NOT NULL,
    timeframe TEXT NOT NULL,
    open NUMERIC(20, 6) NOT NULL,
    high NUMERIC(20, 6) NOT NULL,
    low NUMERIC(20, 6) NOT NULL,
    close NUMERIC(20, 6) NOT NULL,
    volume NUMERIC(30, 6),
    source TEXT NOT NULL,
    PRIMARY KEY (instrument_id, observed_at, timeframe)
);
SELECT create_hypertable('price_bar', 'observed_at', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS institutional_change (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    instrument_id UUID NOT NULL REFERENCES instrument(id),
    action TEXT NOT NULL,
    disclosed_weight NUMERIC(8, 4),
    estimated_change NUMERIC(8, 4),
    observed_on DATE NOT NULL,
    source_url TEXT,
    source_kind TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (account_name, instrument_id, action, observed_on, source_hash)
);

CREATE TABLE IF NOT EXISTS research_citation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT,
    published_at TIMESTAMPTZ,
    retrieved_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    content_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alert (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspace(id) ON DELETE CASCADE,
    alert_type TEXT NOT NULL,
    severity alert_severity NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    dedupe_key TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    read_at TIMESTAMPTZ,
    UNIQUE (workspace_id, dedupe_key)
);

CREATE TABLE IF NOT EXISTS audit_event (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspace(id),
    actor_id UUID REFERENCES app_user(id),
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS price_bar_instrument_time_idx ON price_bar (instrument_id, observed_at DESC);
CREATE INDEX IF NOT EXISTS institutional_change_observed_idx ON institutional_change (observed_on DESC);
CREATE INDEX IF NOT EXISTS audit_event_workspace_time_idx ON audit_event (workspace_id, created_at DESC);
