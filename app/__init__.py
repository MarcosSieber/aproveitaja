"""AproveitaJá - fábrica da aplicação Flask (padrão MVC)."""
import os

from flask import Flask, render_template

from .models import database


def create_app(config=None):
    app = Flask(__name__, template_folder="views", instance_relative_config=True)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao"),
        DATABASE=os.path.join(app.instance_path, "aproveitaja.db"),
    )
    if config:
        app.config.update(config)

    database.init_app(app)

    from .controllers import auth_controller, dashboard_controller, produto_controller
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(dashboard_controller.bp)
    app.register_blueprint(produto_controller.bp)

    @app.template_filter("qtd")
    def formatar_quantidade(valor):
        return f"{valor:g}".replace(".", ",")

    @app.template_filter("moeda")
    def formatar_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @app.template_filter("data_br")
    def formatar_data(valor):
        ano, mes, dia = str(valor)[:10].split("-")
        return f"{dia}/{mes}/{ano}"

    @app.errorhandler(404)
    def nao_encontrado(_e):
        return render_template("404.html"), 404

    return app
