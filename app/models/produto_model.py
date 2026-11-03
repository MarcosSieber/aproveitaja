"""Model de Produto: cadastro, validação, consultas e status de validade."""
from datetime import date, datetime, timedelta

from .database import get_db

CATEGORIAS = ["Hortifrúti", "Padaria", "Laticínios", "Carnes", "Mercearia", "Bebidas", "Outros"]
UNIDADES = ["un", "kg", "L"]
DIAS_ATENCAO = 3  # produtos que vencem em até 3 dias entram em alerta


def status_validade(data_validade, hoje=None):
    """Classifica o produto em 'vencido', 'atencao' ou 'ok'."""
    hoje = hoje or date.today()
    validade = _para_data(data_validade)
    if validade < hoje:
        return "vencido"
    if validade <= hoje + timedelta(days=DIAS_ATENCAO):
        return "atencao"
    return "ok"


def dias_para_vencer(data_validade, hoje=None):
    hoje = hoje or date.today()
    return (_para_data(data_validade) - hoje).days


def validar(dados, novo=True, hoje=None):
    """Valida os campos do formulário. Retorna (dados_limpos, erros)."""
    hoje = hoje or date.today()
    erros = []
    limpo = {}

    nome = (dados.get("nome") or "").strip()
    if len(nome) < 2 or len(nome) > 100:
        erros.append("O nome do produto deve ter entre 2 e 100 caracteres.")
    limpo["nome"] = nome

    categoria = dados.get("categoria")
    if categoria not in CATEGORIAS:
        erros.append("Selecione uma categoria válida.")
    limpo["categoria"] = categoria

    unidade = dados.get("unidade")
    if unidade not in UNIDADES:
        erros.append("Selecione uma unidade válida (un, kg ou L).")
    limpo["unidade"] = unidade

    try:
        quantidade = float(str(dados.get("quantidade", "")).replace(",", "."))
        # Correção BUG-02: quantidade zero ou negativa não é aceita
        if quantidade <= 0:
            raise ValueError
        limpo["quantidade"] = quantidade
    except ValueError:
        erros.append("A quantidade deve ser um número maior que zero.")

    try:
        preco = float(str(dados.get("preco") or "0").replace(",", "."))
        if preco < 0:
            raise ValueError
        limpo["preco"] = preco
    except ValueError:
        erros.append("O preço deve ser um número igual ou maior que zero.")

    try:
        validade = _para_data(dados.get("data_validade"))
        # Correção BUG-01: não aceitar cadastro de produto já vencido
        if novo and validade < hoje:
            erros.append("A data de validade não pode estar no passado.")
        limpo["data_validade"] = validade.isoformat()
    except (TypeError, ValueError):
        erros.append("Informe uma data de validade válida.")

    return limpo, erros


def criar(usuario_id, dados):
    db = get_db()
    cur = db.execute(
        """INSERT INTO produtos (usuario_id, nome, categoria, quantidade, unidade, data_validade, preco)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (usuario_id, dados["nome"], dados["categoria"], dados["quantidade"],
         dados["unidade"], dados["data_validade"], dados["preco"]),
    )
    db.commit()
    return cur.lastrowid


def atualizar(produto_id, usuario_id, dados):
    db = get_db()
    db.execute(
        """UPDATE produtos SET nome = ?, categoria = ?, quantidade = ?, unidade = ?,
                  data_validade = ?, preco = ?
           WHERE id = ? AND usuario_id = ?""",
        (dados["nome"], dados["categoria"], dados["quantidade"], dados["unidade"],
         dados["data_validade"], dados["preco"], produto_id, usuario_id),
    )
    db.commit()


def excluir(produto_id, usuario_id):
    db = get_db()
    db.execute("DELETE FROM produtos WHERE id = ? AND usuario_id = ?", (produto_id, usuario_id))
    db.commit()


def buscar(produto_id, usuario_id):
    return get_db().execute(
        "SELECT * FROM produtos WHERE id = ? AND usuario_id = ?", (produto_id, usuario_id)
    ).fetchone()


def listar(usuario_id, busca=None, status=None, hoje=None):
    """Lista produtos em estoque ordenados pela validade (melhoria SUG-01 e SUG-02)."""
    sql = "SELECT * FROM produtos WHERE usuario_id = ? AND quantidade > 0"
    params = [usuario_id]
    if busca:
        sql += " AND nome LIKE ?"
        params.append(f"%{busca.strip()}%")
    sql += " ORDER BY data_validade ASC, nome ASC"
    linhas = get_db().execute(sql, params).fetchall()
    produtos = []
    for linha in linhas:
        p = dict(linha)
        p["status"] = status_validade(p["data_validade"], hoje)
        p["dias"] = dias_para_vencer(p["data_validade"], hoje)
        if status and p["status"] != status:
            continue
        produtos.append(p)
    return produtos


def resumo(usuario_id, hoje=None):
    contagem = {"vencido": 0, "atencao": 0, "ok": 0}
    for p in listar(usuario_id, hoje=hoje):
        contagem[p["status"]] += 1
    contagem["total"] = sum(contagem.values())
    return contagem


def _para_data(valor):
    if isinstance(valor, date):
        return valor
    return datetime.strptime(str(valor), "%Y-%m-%d").date()
