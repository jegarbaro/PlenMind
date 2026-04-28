-- ================================================
-- PlenMind - Esquema de base de datos
-- ================================================

CREATE EXTENSION IF NOT EXISTS vector;

-- ─────────────── ÁREAS ───────────────
CREATE TABLE IF NOT EXISTS areas (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL UNIQUE,
    slug            VARCHAR(50) NOT NULL UNIQUE,
    descripcion     TEXT,
    color_hex       VARCHAR(7) DEFAULT '#FF8204',
    idioma_default  VARCHAR(2) DEFAULT 'es',
    activa          BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ─────────────── USUARIOS ───────────────
CREATE TABLE IF NOT EXISTS usuarios (
    id                       SERIAL PRIMARY KEY,
    email                    VARCHAR(200) NOT NULL UNIQUE,
    nombre                   VARCHAR(200),
    rol                      VARCHAR(20) DEFAULT 'empleado'
                             CHECK (rol IN ('empleado','responsable_area','manager','admin')),
    area_responsabilidad_id  INTEGER REFERENCES areas(id),
    activo                   BOOLEAN DEFAULT TRUE,
    last_login               TIMESTAMP,
    created_at               TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_one_responsible_per_area
    ON usuarios(area_responsabilidad_id)
    WHERE rol = 'responsable_area' AND activo = TRUE;

-- ─────────────── USUARIO ↔ ÁREAS ───────────────
CREATE TABLE IF NOT EXISTS usuario_areas (
    usuario_id  INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    area_id     INTEGER REFERENCES areas(id) ON DELETE CASCADE,
    permiso     VARCHAR(20) DEFAULT 'lectura'
                CHECK (permiso IN ('lectura','escritura','admin')),
    granted_at  TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (usuario_id, area_id)
);

-- ─────────────── DOCUMENTOS ───────────────
CREATE TABLE IF NOT EXISTS documents (
    id                SERIAL PRIMARY KEY,
    area_id           INTEGER REFERENCES areas(id),
    document_group_id UUID DEFAULT gen_random_uuid(),
    titulo            VARCHAR(500) NOT NULL,
    filename          VARCHAR(500),
    file_hash         VARCHAR(64),
    file_path         TEXT,
    page_count        INTEGER,
    idioma            VARCHAR(2) DEFAULT 'es',
    autor             VARCHAR(200),
    autor_id          INTEGER REFERENCES usuarios(id),
    version           VARCHAR(20) DEFAULT 'v1',
    status            VARCHAR(20) DEFAULT 'activo'
                      CHECK (status IN ('activo','obsoleto','borrador','archivado')),
    replaces          INTEGER REFERENCES documents(id),
    replaced_by       INTEGER REFERENCES documents(id),
    visibility        VARCHAR(20) DEFAULT 'area',
    valid_from        DATE,
    valid_until       DATE,
    tags              TEXT[],
    cluster_id        INTEGER,
    notas_cambio      TEXT,
    created_at        TIMESTAMP DEFAULT NOW(),
    updated_at        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_docs_area ON documents(area_id);
CREATE INDEX IF NOT EXISTS idx_docs_status ON documents(status) WHERE status = 'activo';
CREATE INDEX IF NOT EXISTS idx_docs_group ON documents(document_group_id);
CREATE INDEX IF NOT EXISTS idx_docs_hash ON documents(file_hash);

-- ─────────────── CHUNKS VECTORIALES ───────────────
CREATE TABLE IF NOT EXISTS chunks (
    id           BIGSERIAL PRIMARY KEY,
    document_id  INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index  INTEGER NOT NULL,
    content      TEXT NOT NULL,
    page_number  INTEGER,
    section      VARCHAR(200),
    embedding    vector(384),
    is_image     BOOLEAN DEFAULT FALSE,
    image_path   TEXT,
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(document_id);

-- ─────────────── CONSULTAS ───────────────
CREATE TABLE IF NOT EXISTS consultas (
    id              BIGSERIAL PRIMARY KEY,
    usuario_id      INTEGER REFERENCES usuarios(id),
    area_id         INTEGER REFERENCES areas(id),
    pregunta        TEXT NOT NULL,
    pregunta_idioma VARCHAR(2),
    respuesta       TEXT,
    chunks_usados   INTEGER[],
    proveedor       VARCHAR(50),
    modelo          VARCHAR(100),
    tokens_input    INTEGER,
    tokens_output   INTEGER,
    coste           DECIMAL(10,6) DEFAULT 0,
    duracion_ms     INTEGER,
    rating          INTEGER,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ─────────────── PROVEEDORES Y PRECIOS ───────────────
CREATE TABLE IF NOT EXISTS provider_config (
    id                  SERIAL PRIMARY KEY,
    provider            VARCHAR(50),
    task                VARCHAR(50),
    model               VARCHAR(100),
    is_active           BOOLEAN DEFAULT FALSE,
    is_default          BOOLEAN DEFAULT FALSE,
    api_key_encrypted   TEXT,
    config              JSONB,
    updated_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS model_pricing (
    id                       SERIAL PRIMARY KEY,
    provider                 VARCHAR(50),
    model                    VARCHAR(100),
    price_input_per_1m       DECIMAL(10,4) DEFAULT 0,
    price_output_per_1m      DECIMAL(10,4) DEFAULT 0,
    price_image              DECIMAL(10,4) DEFAULT 0,
    currency                 VARCHAR(3) DEFAULT 'EUR',
    updated_at               TIMESTAMP DEFAULT NOW()
);

-- ─────────────── AUDITORÍA Y TRACKING ───────────────
CREATE TABLE IF NOT EXISTS usage_log (
    id                BIGSERIAL PRIMARY KEY,
    timestamp         TIMESTAMP DEFAULT NOW(),
    area_id           INTEGER REFERENCES areas(id),
    usuario_id        INTEGER REFERENCES usuarios(id),
    task_type         VARCHAR(50),
    provider          VARCHAR(50),
    model             VARCHAR(100),
    tokens_input      INTEGER,
    tokens_output     INTEGER,
    images_processed  INTEGER,
    cost_total        DECIMAL(10,6),
    consulta_id       INTEGER REFERENCES consultas(id)
);

CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON usage_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_usage_area ON usage_log(area_id, timestamp);

CREATE TABLE IF NOT EXISTS budget_config (
    id                   SERIAL PRIMARY KEY,
    monthly_limit_eur    DECIMAL(10,2),
    alert_threshold      DECIMAL(3,2) DEFAULT 0.80,
    block_on_limit       BOOLEAN DEFAULT FALSE,
    email_daily_report   BOOLEAN DEFAULT FALSE,
    alert_emails         TEXT[],
    updated_at           TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_log (
    id              BIGSERIAL PRIMARY KEY,
    timestamp       TIMESTAMP DEFAULT NOW(),
    usuario_id      INTEGER,
    usuario_email   VARCHAR(200),
    action          VARCHAR(100),
    resource_type   VARCHAR(50),
    resource_id     INTEGER,
    area_id         INTEGER,
    details         JSONB,
    ip_address      VARCHAR(45),
    user_agent      TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(usuario_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action, timestamp);

-- ─────────────── DATOS INICIALES ───────────────
INSERT INTO areas (nombre, slug, descripcion, color_hex, idioma_default, activa)
VALUES ('PlenMind OPS', 'ops', 'Operaciones IT - procedimientos, runbooks y arquitecturas', '#FF8204', 'es', TRUE)
ON CONFLICT (slug) DO NOTHING;

INSERT INTO areas (nombre, slug, descripcion, color_hex, idioma_default, activa)
VALUES ('PlenMind Infra', 'infra', 'Infraestructura IT', '#002D74', 'es', FALSE)
ON CONFLICT (slug) DO NOTHING;

INSERT INTO usuarios (email, nombre, rol)
VALUES ('admin@plenergy.es', 'Admin Plenergy', 'admin')
ON CONFLICT (email) DO NOTHING;

INSERT INTO model_pricing (provider, model, price_input_per_1m, price_output_per_1m, currency)
VALUES 
    ('ollama', 'llama3.1:8b', 0, 0, 'EUR'),
    ('ollama', 'llava:7b', 0, 0, 'EUR'),
    ('anthropic', 'claude-haiku-4', 0.80, 4.00, 'EUR'),
    ('anthropic', 'claude-sonnet-4', 3.00, 15.00, 'EUR'),
    ('anthropic', 'claude-opus-4', 15.00, 75.00, 'EUR')
ON CONFLICT DO NOTHING;
