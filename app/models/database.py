"""Conexão com o banco de dados SQLite."""
import os
import sqlite3

from flask import current_app, g

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database", "schema.sql")


def get_db():
    """Retorna a conexão da requisição atual (uma por requisição)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas a partir de database/schema.sql."""
    db = get_db()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        """Apaga e recria o banco de dados."""
        init_db()
        print("Banco de dados criado com sucesso.")

    # Cria o banco automaticamente na primeira execução
    if not os.path.exists(app.config["DATABASE"]):
        os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
        with app.app_context():
            init_db()
