"""Model de Destinação: registra para onde foi o produto próximo do vencimento."""
from .database import get_db

TIPOS = {
    "promocao": "Venda em promoção",
    "doacao": "Doação",
    "reaproveitamento": "Reaproveitamento (receitas/produção)",
    "descarte": "Descarte",
}
TIPOS_APROVEITADOS = ("promocao", "doacao", "reaproveitamento")


def validar(dados, estoque):
    erros = []
    tipo = dados.get("tipo")
    if tipo not in TIPOS:
        erros.append("Selecione um tipo de destinação válido.")
    quantidade = None
    try:
        quantidade = float(str(dados.get("quantidade", "")).replace(",", "."))
        if quantidade <= 0:
            erros.append("A quantidade deve ser maior que zero.")
        # Correção BUG-03: não permitir destinar mais do que existe em estoque
        elif quantidade > estoque:
            erros.append(f"A quantidade não pode ser maior que o estoque atual ({estoque:g}).")
    except ValueError:
        erros.append("Informe uma quantidade numérica.")
    observacao = (dados.get("observacao") or "").strip()[:255]
    return {"tipo": tipo, "quantidade": quantidade, "observacao": observacao}, erros


def registrar(produto_id, dados):
    """Registra a destinação e baixa o estoque na mesma transação."""
    db = get_db()
    with db:
        db.execute(
            "INSERT INTO destinacoes (produto_id, tipo, quantidade, observacao) VALUES (?, ?, ?, ?)",
            (produto_id, dados["tipo"], dados["quantidade"], dados["observacao"]),
        )
        db.execute(
            "UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",
            (dados["quantidade"], produto_id),
        )


def relatorio(usuario_id):
    linhas = get_db().execute(
        """SELECT d.tipo, COUNT(*) AS registros, SUM(d.quantidade) AS quantidade,
                  SUM(d.quantidade * p.preco) AS valor
           FROM destinacoes d JOIN produtos p ON p.id = d.produto_id
           WHERE p.usuario_id = ?
           GROUP BY d.tipo""",
        (usuario_id,),
    ).fetchall()
    por_tipo = {t: {"rotulo": r, "registros": 0, "quantidade": 0.0, "valor": 0.0} for t, r in TIPOS.items()}
    for linha in linhas:
        por_tipo[linha["tipo"]].update(
            registros=linha["registros"], quantidade=linha["quantidade"] or 0, valor=linha["valor"] or 0
        )
    total = sum(v["quantidade"] for v in por_tipo.values())
    aproveitado = sum(por_tipo[t]["quantidade"] for t in TIPOS_APROVEITADOS)
    return {
        "por_tipo": por_tipo,
        "total": total,
        "aproveitado": aproveitado,
        "percentual": round(aproveitado / total * 100, 1) if total else 0.0,
        "valor_recuperado": por_tipo["promocao"]["valor"],
    }


def historico(usuario_id, limite=20):
    return get_db().execute(
        """SELECT d.*, p.nome AS produto, p.unidade
           FROM destinacoes d JOIN produtos p ON p.id = d.produto_id
           WHERE p.usuario_id = ?
           ORDER BY d.id DESC LIMIT ?""",
        (usuario_id, limite),
    ).fetchall()
