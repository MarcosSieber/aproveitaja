import os
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.models import database  # noqa: E402


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "teste.db"), "SECRET_KEY": "teste"})
    with app.app_context():
        database.init_db()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def dia(delta):
    """Data relativa a hoje no formato do formulário (AAAA-MM-DD)."""
    return (date.today() + timedelta(days=delta)).isoformat()


def cadastrar(client, nome="Mercado Teste", email="teste@mercado.com", senha="senha123"):
    return client.post("/cadastro", data={
        "nome": nome, "email": email, "senha": senha, "confirmacao": senha,
    }, follow_redirects=True)


def criar_produto(client, **campos):
    dados = {"nome": "Banana", "categoria": "Hortifrúti", "quantidade": "10",
             "unidade": "kg", "data_validade": dia(10), "preco": "5.00"}
    dados.update(campos)
    return client.post("/produtos/novo", data=dados, follow_redirects=True)


@pytest.fixture
def logado(client):
    cadastrar(client)
    return client
