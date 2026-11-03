"""Controller de produtos: CRUD e registro de destinação."""
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from ..models import destinacao_model, produto_model
from .auth_controller import login_obrigatorio

bp = Blueprint("produtos", __name__, url_prefix="/produtos")


def _produto_ou_404(produto_id):
    produto = produto_model.buscar(produto_id, g.usuario["id"])
    if produto is None:
        abort(404)
    return produto


@bp.route("/")
@login_obrigatorio
def listar():
    busca = request.args.get("busca", "").strip()
    status = request.args.get("status") or None
    produtos = produto_model.listar(g.usuario["id"], busca=busca, status=status)
    return render_template("produtos.html", produtos=produtos, busca=busca, status=status)


@bp.route("/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo():
    if request.method == "POST":
        dados, erros = produto_model.validar(request.form, novo=True)
        if not erros:
            produto_model.criar(g.usuario["id"], dados)
            flash(f"Produto \"{dados['nome']}\" cadastrado com sucesso.", "sucesso")
            return redirect(url_for("produtos.listar"))
        for e in erros:
            flash(e, "erro")
        return _form(request.form, "Novo produto"), 400
    return _form({}, "Novo produto")


@bp.route("/<int:produto_id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar(produto_id):
    produto = _produto_ou_404(produto_id)
    if request.method == "POST":
        dados, erros = produto_model.validar(request.form, novo=False)
        if not erros:
            produto_model.atualizar(produto_id, g.usuario["id"], dados)
            flash("Produto atualizado com sucesso.", "sucesso")
            return redirect(url_for("produtos.listar"))
        for e in erros:
            flash(e, "erro")
        return _form(request.form, "Editar produto", produto_id), 400
    return _form(dict(produto), "Editar produto", produto_id)


@bp.route("/<int:produto_id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir(produto_id):
    produto = _produto_ou_404(produto_id)
    produto_model.excluir(produto_id, g.usuario["id"])
    flash(f"Produto \"{produto['nome']}\" excluído.", "sucesso")
    return redirect(url_for("produtos.listar"))


@bp.route("/<int:produto_id>/destinar", methods=["GET", "POST"])
@login_obrigatorio
def destinar(produto_id):
    produto = _produto_ou_404(produto_id)
    if request.method == "POST":
        dados, erros = destinacao_model.validar(request.form, produto["quantidade"])
        if not erros:
            destinacao_model.registrar(produto_id, dados)
            flash(f"Destinação registrada: {destinacao_model.TIPOS[dados['tipo']]}.", "sucesso")
            return redirect(url_for("dashboard.index"))
        for e in erros:
            flash(e, "erro")
        return render_template("destinar.html", produto=produto, tipos=destinacao_model.TIPOS, form=request.form), 400
    return render_template("destinar.html", produto=produto, tipos=destinacao_model.TIPOS, form={})


def _form(form, titulo, produto_id=None):
    return render_template(
        "produto_form.html", form=form, titulo=titulo, produto_id=produto_id,
        categorias=produto_model.CATEGORIAS, unidades=produto_model.UNIDADES,
    )
