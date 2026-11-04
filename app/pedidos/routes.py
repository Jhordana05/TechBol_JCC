
from flask import render_template, request, redirect, url_for, flash
from app.pedidos import bp_pedidos
from app.extensions import db
from app.models import Pedido, Cliente, Producto
from datetime import datetime


# Mostrar pedidos
@bp_pedidos.route('/')
def listar_pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos/listar.html', pedidos=pedidos)


# Registrar pedido
@bp_pedidos.route('/crear', methods=['GET', 'POST'])
def crear_pedido():
    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':
        cliente_id = int(request.form['cliente_id'])
        producto_id = int(request.form['producto_id'])
        cantidad = int(request.form['cantidad'])

        cliente = db.session.get(Cliente, cliente_id)
        producto = db.session.get(Producto, producto_id)

        if cliente is None or producto is None:
            flash('Seleccione un cliente y un producto válidos', 'danger')
            return redirect(url_for('pedidos.crear_pedido'))

        if cantidad <= 0:
            flash('La cantidad debe ser mayor a cero', 'danger')
            return redirect(url_for('pedidos.crear_pedido'))

        if producto.stock < cantidad:
            flash('No hay suficiente stock disponible', 'danger')
            return redirect(url_for('pedidos.crear_pedido'))

        monto = producto.precio * cantidad

        pedido = Pedido(
            fecha=datetime.now(),
            monto=monto,
            producto_id=producto.id,
            cliente_id=cliente.id
        )

        producto.stock -= cantidad

        db.session.add(pedido)
        db.session.commit()

        flash('Pedido registrado correctamente', 'success')
        return redirect(url_for('pedidos.listar_pedidos'))

    return render_template(
        'pedidos/crear.html',
        clientes=clientes,
        productos=productos
    )


# Eliminar pedido
@bp_pedidos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_pedido(id):
    pedido = db.session.get(Pedido, id)

    if pedido is not None:
        db.session.delete(pedido)
        db.session.commit()
        flash('Pedido eliminado correctamente', 'success')

    return redirect(url_for('pedidos.listar_pedidos'))
