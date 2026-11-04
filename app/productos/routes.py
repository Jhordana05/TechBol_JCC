
from flask import render_template, request, redirect, url_for, flash

from app.productos import bp_productos
from app.extensions import db
from app.models import Producto


@bp_productos.route('/')
def listar_productos():

    productos = Producto.query.all()

    return render_template(
        'productos/listar.html',
        productos=productos
    )


@bp_productos.route('/crear', methods=['GET', 'POST'])
def crear_producto():

    if request.method == 'POST':

        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock
        )

        db.session.add(producto)
        db.session.commit()

        flash('Producto registrado correctamente', 'success')

        return redirect(url_for('productos.listar_productos'))

    return render_template('productos/crear.html')


@bp_productos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    producto = db.session.get(Producto, id)

    if producto is None:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos.listar_productos'))

    if request.method == 'POST':

        producto.nombre = request.form['nombre']
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])

        db.session.commit()

        flash('Producto actualizado correctamente', 'success')

        return redirect(url_for('productos.listar_productos'))

    return render_template(
        'productos/editar.html',
        producto=producto
    )


@bp_productos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):

    producto = db.session.get(Producto, id)

    if producto is not None:

        db.session.delete(producto)
        db.session.commit()

        flash('Producto eliminado correctamente', 'success')

    return redirect(url_for('productos.listar_productos'))
