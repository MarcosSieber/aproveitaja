"""Model de Usuário: cadastro, validação e autenticação."""
import re
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SENHA_MINIMA = 6


def validar_cadastro(nome, email, senha, confirmacao):
    erros = []
    if not nome or len(nome.strip()) < 3:
        erros.append("Informe seu nome completo (mínimo de 3 caracteres).")
    if not email or not EMAIL_RE.match(email.strip()):
        erros.append("Informe um e-mail válido.")
    if not senha or len(senha) < SENHA_MINIMA:
        erros.append(f"A senha deve ter pelo menos {SENHA_MINIMA} caracteres.")
    elif senha != confirmacao:
        erros.append("A confirmação de senha não confere.")
    return erros


def criar(nome, email, senha):
    """Cria o usuário. Retorna (id, None) ou (None, mensagem_de_erro)."""
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
            (nome.strip(), email.strip().lower(), generate_password_hash(senha)),
        )
        db.commit()
        return cur.lastrowid, None
    except sqlite3.IntegrityError:
        return None, "Este e-mail já está cadastrado. Faça login ou use outro e-mail."


def autenticar(email, senha):
    usuario = buscar_por_email(email)
    if usuario and check_password_hash(usuario["senha_hash"], senha or ""):
        return usuario
    return None


def buscar_por_email(email):
    return get_db().execute(
        "SELECT * FROM usuarios WHERE email = ?", ((email or "").strip().lower(),)
    ).fetchone()


def buscar_por_id(usuario_id):
    return get_db().execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
