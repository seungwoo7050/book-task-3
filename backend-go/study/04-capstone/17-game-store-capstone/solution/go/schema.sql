-- Game Store Capstone schema (PostgreSQL/Cockroach-compatible SQL)

CREATE TABLE IF NOT EXISTS players (
    id         UUID PRIMARY KEY,
    name       TEXT NOT NULL,
    balance    BIGINT NOT NULL CHECK (balance >= 0),
    version    BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS catalog_items (
    id         UUID PRIMARY KEY,
    sku        TEXT NOT NULL UNIQUE,
    name       TEXT NOT NULL,
    price      BIGINT NOT NULL CHECK (price > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS purchases (
    id         UUID PRIMARY KEY,
    player_id  UUID NOT NULL REFERENCES players(id),
    item_id    UUID NOT NULL REFERENCES catalog_items(id),
    price      BIGINT NOT NULL CHECK (price > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS inventories (
    id         UUID PRIMARY KEY,
    player_id  UUID NOT NULL REFERENCES players(id),
    item_id    UUID NOT NULL REFERENCES catalog_items(id),
    qty        INT NOT NULL CHECK (qty >= 0),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (player_id, item_id)
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
    key           TEXT PRIMARY KEY,
    request_hash  TEXT NOT NULL,
    response_json JSONB NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS outbox (
    id           UUID PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type   TEXT NOT NULL,
    payload_json JSONB NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS outbox_unpublished_idx
    ON outbox (published_at, created_at);

INSERT INTO players (id, name, balance, version)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'alice', 5000, 0),
    ('22222222-2222-2222-2222-222222222222', 'bob', 2000, 0)
ON CONFLICT (id) DO NOTHING;

INSERT INTO catalog_items (id, sku, name, price)
VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'sword-basic', 'Bronze Sword', 1000),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'shield-basic', 'Wood Shield', 1500),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'potion-hp', 'HP Potion', 300)
ON CONFLICT (id) DO NOTHING;
