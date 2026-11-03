"""Controller de autenticação: cadastro, login e logout."""
from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from ..models import usuario_model

bp = Blueprint("auth", __name__)


def login_obrigatorio(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.get("usuario") is None:
            flash("Faça login para acessar esta página.", "aviso")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapper


@bp.before_app_request
def carregar_usuario():
    usuario_id = session.get("usuario_id")
    g.usuario = usuario_model.buscar_por_id(usuario_id) if usuario_id else None


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        f = request.form
        erros = usuario_model.validar_cadastro(f.get("nome"), f.get("email"), f.get("senha"), f.get("confirmacao"))
        if not erros:
            usuario_id, erro = usuario_model.criar(f["nome"], f["email"], f["senha"])
            if erro:
                erros.append(erro)
            else:
                session.clear()
                session["usuario_id"] = usuario_id
                flash("Conta criada com sucesso! Bem-vindo(a) ao AproveitaJá.", "sucesso")
                return redirect(url_for("dashboard.index"))
        for e in erros:
            flash(e, "erro")
        return render_template("cadastro.html", form=f), 400
    return render_template("cadastro.html", form={})


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = usuario_model.autenticar(request.form.get("email"), request.form.get("senha"))
        if usuario:
            session.clear()
            session["usuario_id"] = usuario["id"]
            return redirect(url_for("dashboard.index"))
        # Melhoria SUG-04: mensagem de erro clara, sem revelar qual campo está errado
        flash("E-mail ou senha incorretos. Verifique os dados e tente novamente.", "erro")
        return render_template("login.html", email=request.form.get("email", "")), 401
    return render_template("login.html", email="")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("auth.login"))
