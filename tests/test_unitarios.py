"""Testes unitários das regras de negócio (camada Model)."""
from datetime import date, timedelta

import pytest

from app.models import destinacao_model, produto_model, usuario_model

HOJE = date(2026, 10, 1)


def produto_valido(**campos):
    dados = {"nome": "Tomate", "categoria": "Hortifrúti", "quantidade": "5",
             "unidade": "kg", "data_validade": "2026-10-10", "preco": "8.90"}
    dados.update(campos)
    return dados


# ---------- Status de validade ----------
@pytest.mark.parametrize("delta, esperado", [
    (-1, "vencido"),
    (0, "atencao"),
    (3, "atencao"),   # limite de alerta
    (4, "ok"),
    (30, "ok"),
])
def test_status_validade(delta, esperado):
    validade = (HOJE + timedelta(days=delta)).isoformat()
    assert produto_model.status_validade(validade, hoje=HOJE) == esperado


def test_dias_para_vencer():
    assert produto_model.dias_para_vencer("2026-10-05", hoje=HOJE) == 4


# ---------- Validação de produto ----------
def test_produto_valido_sem_erros():
    limpo, erros = produto_model.validar(produto_valido(), hoje=HOJE)
    assert erros == []
    assert limpo["quantidade"] == 5.0 and limpo["preco"] == 8.90


def test_produto_aceita_virgula_decimal():
    limpo, erros = produto_model.validar(produto_valido(quantidade="2,5", preco="3,49"), hoje=HOJE)
    assert erros == []
    assert limpo["quantidade"] == 2.5 and limpo["preco"] == 3.49


@pytest.mark.parametrize("campo, valor", [
    ("nome", ""),
    ("nome", "x"),
    ("categoria", "Eletrônicos"),
    ("unidade", "caixa"),
    ("quantidade", "0"),
    ("quantidade", "-3"),
    ("quantidade", "abc"),
    ("preco", "-1"),
    ("data_validade", "31/12/2026"),
])
def test_produto_campo_invalido(campo, valor):
    _, erros = produto_model.validar(produto_valido(**{campo: valor}), hoje=HOJE)
    assert len(erros) == 1


def test_bug01_cadastro_com_validade_no_passado_e_rejeitado():
    _, erros = produto_model.validar(produto_valido(data_validade="2026-09-30"), novo=True, hoje=HOJE)
    assert "A data de validade não pode estar no passado." in erros


def test_edicao_de_produto_ja_vencido_e_permitida():
    _, erros = produto_model.validar(produto_valido(data_validade="2026-09-30"), novo=False, hoje=HOJE)
    assert erros == []


# ---------- Validação de cadastro de usuário ----------
def test_cadastro_usuario_valido():
    assert usuario_model.validar_cadastro("Maria Silva", "maria@email.com", "segura1", "segura1") == []


@pytest.mark.parametrize("nome, email, senha, confirmacao", [
    ("Ma", "maria@email.com", "segura1", "segura1"),
    ("Maria", "email-invalido", "segura1", "segura1"),
    ("Maria", "maria@email.com", "123", "123"),
    ("Maria", "maria@email.com", "segura1", "outra12"),
])
def test_cadastro_usuario_invalido(nome, email, senha, confirmacao):
    assert len(usuario_model.validar_cadastro(nome, email, senha, confirmacao)) == 1


# ---------- Validação de destinação ----------
def test_destinacao_valida():
    dados, erros = destinacao_model.validar({"tipo": "doacao", "quantidade": "2"}, estoque=5)
    assert erros == [] and dados["quantidade"] == 2


def test_bug03_destinacao_maior_que_estoque_e_rejeitada():
    _, erros = destinacao_model.validar({"tipo": "doacao", "quantidade": "6"}, estoque=5)
    assert "maior que o estoque" in erros[0]


@pytest.mark.parametrize("dados", [
    {"tipo": "lixo", "quantidade": "1"},
    {"tipo": "doacao", "quantidade": "0"},
    {"tipo": "doacao", "quantidade": "dois"},
])
def test_destinacao_invalida(dados):
    _, erros = destinacao_model.validar(dados, estoque=5)
    assert len(erros) == 1
