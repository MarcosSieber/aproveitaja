"""Controller do painel, relatório e dicas."""
from flask import Blueprint, g, redirect, render_template, url_for

from ..models import destinacao_model, dica_model, produto_model
from .auth_controller import login_obrigatorio

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def inicio():
    if g.get("usuario"):
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))


@bp.route("/painel")
@login_obrigatorio
def index():
    usuario_id = g.usuario["id"]
    resumo = produto_model.resumo(usuario_id)
    alertas = [p for p in produto_model.listar(usuario_id) if p["status"] != "ok"]
    return render_template("dashboard.html", resumo=resumo, alertas=alertas)


@bp.route("/relatorio")
@login_obrigatorio
def relatorio():
    usuario_id = g.usuario["id"]
    return render_template(
        "relatorio.html",
        dados=destinacao_model.relatorio(usuario_id),
        historico=destinacao_model.historico(usuario_id),
        tipos=destinacao_model.TIPOS,
    )


@bp.route("/dicas")
@login_obrigatorio
def dicas():
    return render_template("dicas.html", dicas=dica_model.DICAS)
