-- AproveitaJá - Esquema do banco de dados (SQLite)
-- Projeto físico gerado a partir do modelo lógico normalizado (3FN).

DROP TABLE IF EXISTS destinacoes;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    senha_hash  TEXT    NOT NULL,
    criado_em   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE produtos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id     INTEGER NOT NULL REFERENCES usuarios (id) ON DELETE CASCADE,
    nome           TEXT    NOT NULL,
    categoria      TEXT    NOT NULL,
    quantidade     REAL    NOT NULL CHECK (quantidade >= 0),
    unidade        TEXT    NOT NULL CHECK (unidade IN ('un', 'kg', 'L')),
    data_validade  TEXT    NOT NULL,
    preco          REAL    NOT NULL DEFAULT 0 CHECK (preco >= 0),
    criado_em      TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE destinacoes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id  INTEGER NOT NULL REFERENCES produtos (id) ON DELETE CASCADE,
    tipo        TEXT    NOT NULL CHECK (tipo IN ('promocao', 'doacao', 'reaproveitamento', 'descarte')),
    quantidade  REAL    NOT NULL CHECK (quantidade > 0),
    observacao  TEXT,
    data        TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX idx_produtos_usuario   ON produtos (usuario_id);
CREATE INDEX idx_produtos_validade  ON produtos (data_validade);
CREATE INDEX idx_destinacoes_prod   ON destinacoes (produto_id);
