
from app.extensions import db
from datetime import datetime


class Pedido(db.Model):

    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    monto = db.Column(db.Float, nullable=False)

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey('productos.id'),
        nullable=False
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey('clientes.id'),
        nullable=False
    )

    producto = db.relationship(
        'Producto',
        back_populates='pedidos'
    )

    cliente = db.relationship(
        'Cliente',
        back_populates='pedidos'
    )

    def __repr__(self):
        return f'<Pedido {self.id}>'
