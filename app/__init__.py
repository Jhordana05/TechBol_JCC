
from flask import Flask
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Cargar modelos
    from app.models import Producto, Cliente, Pedido

    # Registrar Blueprints
    from app.clientes import bp_clientes
    from app.productos import bp_productos
    from app.pedidos import bp_pedidos

    app.register_blueprint(
        bp_clientes,
        url_prefix='/clientes'
    )

    app.register_blueprint(
        bp_productos,
        url_prefix='/productos'
    )

    app.register_blueprint(
        bp_pedidos,
        url_prefix='/pedidos'
    )
    from flask import render_template

    @app.route('/')
    def inicio():
        return render_template('index.html')
    return app
