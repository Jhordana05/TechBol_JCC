from flask import render_template, request, redirect, url_for, flash
from app.clientes import bp_clientes
from app.extensions import db
from app.models import Cliente


# Mostrar clientes
@bp_clientes.route('/')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)


# Registrar cliente
@bp_clientes.route('/crear', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']

        cliente = Cliente(nombre=nombre, telefono=telefono)

        db.session.add(cliente)
        db.session.commit()

        flash('Cliente registrado correctamente', 'success')
        return redirect(url_for('clientes.listar_clientes'))

    return render_template('clientes/crear.html')


# Editar cliente
@bp_clientes.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = db.session.get(Cliente, id)

    if cliente is None:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('clientes.listar_clientes'))

    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.telefono = request.form['telefono']

        db.session.commit()

        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes.listar_clientes'))

    return render_template('clientes/editar.html', cliente=cliente)


# Eliminar cliente
@bp_clientes.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    cliente = db.session.get(Cliente, id)

    if cliente is not None:
        if cliente.pedidos:
            flash('No se puede eliminar porque tiene pedidos registrados', 'danger')
        else:
            db.session.delete(cliente)
            db.session.commit()
            flash('Cliente eliminado correctamente', 'success')

    return redirect(url_for('clientes.listar_clientes'))