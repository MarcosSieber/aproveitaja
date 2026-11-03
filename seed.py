"""Popula o banco com um usuário e produtos de demonstração.

Execute: python seed.py
Login de demonstração: demo@aproveitaja.com / demo123
"""
from datetime import date, timedelta

from app import create_app
from app.models import database, destinacao_model, produto_model, usuario_model

hoje = date.today()

PRODUTOS = [
    ("Banana prata", "Hortifrúti", 12, "kg", 1, 6.99),
    ("Alface crespa", "Hortifrúti", 20, "un", 2, 3.49),
    ("Tomate italiano", "Hortifrúti", 8, "kg", 5, 8.90),
    ("Pão francês", "Padaria", 5, "kg", 0, 16.90),
    ("Iogurte natural 170g", "Laticínios", 30, "un", 3, 2.79),
    ("Queijo muçarela", "Laticínios", 4, "kg", 12, 44.90),
    ("Peito de frango", "Carnes", 10, "kg", 2, 19.90),
    ("Suco de laranja 1L", "Bebidas", 15, "L", 20, 9.49),
]

app = create_app()
with app.app_context():
    database.init_db()
    usuario_id, _ = usuario_model.criar("Mercado Demonstração", "demo@aproveitaja.com", "demo123")
    ids = []
    for nome, cat, qtd, un, dias, preco in PRODUTOS:
        ids.append(produto_model.criar(usuario_id, {
            "nome": nome, "categoria": cat, "quantidade": qtd, "unidade": un,
            "data_validade": (hoje + timedelta(days=dias)).isoformat(), "preco": preco,
        }))
    destinacao_model.registrar(ids[0], {"tipo": "reaproveitamento", "quantidade": 3, "observacao": "Bolo de banana"})
    destinacao_model.registrar(ids[3], {"tipo": "doacao", "quantidade": 2, "observacao": "Doado à ONG do bairro"})
    destinacao_model.registrar(ids[1], {"tipo": "promocao", "quantidade": 8, "observacao": "Leve 2 pague 1"})
    destinacao_model.registrar(ids[1], {"tipo": "descarte", "quantidade": 2, "observacao": "Folhas murchas"})
    print("Banco populado! Login: demo@aproveitaja.com / senha: demo123")
