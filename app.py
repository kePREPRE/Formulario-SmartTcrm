from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)

import os

app.secret_key = os.urandom(24)


# -----------------------------
# Función para conectar a la base de datos
# -----------------------------
def conectar():
    return sqlite3.connect('DB.db')

# -----------------------------
# LOGIN
# -----------------------------

@app.route('/')
def loginI():
    return render_template("login.html")







@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    contra = data.get("contra")

    con = conectar()
    try:
        cursor = con.cursor()
        cursor.execute(
            "SELECT usuario FROM Usuarios WHERE usuario = ? AND contra = ?",
            (usuario, contra)
        )
        row = cursor.fetchone()

        if row:
            session["usuario"] = row[0]  # Guardar sesión
            return jsonify({"success": True, "message": "Login exitoso", "usuario": row[0]})
        else:
            return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401

    finally:
        con.close()


# -----------------------------
# INDEX
# -----------------------------
@app.route('/index')
def index():
    return render_template("index.html")


# -----------------------------
# Rutas principales Para Clientes
# -----------------------------

@app.route('/insertarCliente')
def insertarCliente():
    return render_template("insertarCliente.html")

@app.route('/listaCliente')
def listaCliente():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM clientes")
    lista = cursor.fetchall()
    con.close()
    return render_template('listaCliente.html', listaCliente=lista)


@app.route('/insertar', methods=['POST'])
def insertar():
    try:
        nombre = request.form.get('txtNombreCli')
        correo = request.form.get('txtCorreoCli')
        telefono = request.form.get('txtTelefonoCli')
        direccion = request.form.get('txtDireccionCli')
        provincia = request.form.get('slcProvincias')
        fecha = request.form.get('fecha')

        if not all([nombre, correo, telefono, direccion, provincia, fecha]):
            flash("⚠️ Faltan campos obligatorios", "error")
            return redirect(url_for('index'))

        con = conectar()
        cursor = con.cursor()
        cursor.execute('''
            INSERT INTO Clientes (nombre, correo, telefono, direccion, provincia, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, correo, telefono, direccion, provincia, fecha))
        con.commit()
        con.close()

        flash("✅ Cliente insertado correctamente", "success")
        return redirect(url_for('listaCliente'))

    except Exception as e:
        print("🔥 ERROR en el servidor:", str(e))
        flash(f"❌ Error del servidor: {str(e)}", "error")
        return redirect(url_for('listaCliente'))



    
@app.route('/eliminarCliente/<int:idCliente>', methods=['POST'])
def eliminarCliente(idCliente):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM clientes WHERE idCliente = ?", (idCliente,))
    con.commit()
    con.close()
    return redirect(url_for('listaCliente'))  # O la ruta que quieras mostrar después


@app.route("/editarCliente/<int:idCliente>")
def editarCliente(idCliente):
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Clientes WHERE idCliente = ?", (idCliente,))
    cliente = cursor.fetchone()

    con.close()

    if cliente:
        return render_template("editarCliente.html", cliente=cliente)
    else:
        return "Cliente no encontrado", 404


@app.route('/actualizarCliente', methods=['POST'])
def actualizarCliente():
    try:
        # Capturar campos del formulario (mismos nombres que en el HTML)
        id_cliente = request.form.get('idCliente')
        nombre = request.form.get('txtNombreCli')
        correo = request.form.get('txtCorreoCli')
        telefono = request.form.get('txtTelefonoCli')
        direccion = request.form.get('txtDireccionCli')
        provincia = request.form.get('slcProvincias')
        fecha = request.form.get('fecha')

        # Validación de campos obligatorios
        if not all([id_cliente, nombre, correo, telefono, direccion, provincia, fecha]):
            flash("⚠️ Faltan campos obligatorios", "error")
            return redirect(url_for('listaCliente'))

        # Validación de correo (regex básica)
        import re
        if correo and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            flash("❌ Correo inválido", "error")
            return redirect(url_for('listaCliente'))

        # Validación de teléfono (exactamente 8 dígitos numéricos)
        if telefono and (not telefono.isdigit() or len(telefono) != 8):
            flash("❌ El teléfono debe tener exactamente 8 dígitos numéricos", "error")
            return redirect(url_for('listaCliente'))

        # Validación de fecha
        from datetime import datetime
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            flash("❌ La fecha no tiene un formato válido (AAAA-MM-DD)", "error")
            return redirect(url_for('listaCliente'))

        # ✅ Actualizar en la BD
        con = conectar()
        cursor = con.cursor()
        cursor.execute('''
            UPDATE Clientes 
            SET nombre = ?, correo = ?, telefono = ?, direccion = ?, 
                provincia = ?, fecha_registro = ?
            WHERE idCliente = ?
        ''', (nombre, correo, telefono, direccion, provincia, fecha, id_cliente))
        
        con.commit()
        con.close()

        flash("✅ Cliente actualizado correctamente", "success")
        return redirect(url_for('listaCliente'))

    except Exception as e:
        print("🔥 ERROR en el servidor:", str(e))
        flash(f"❌ Error del servidor: {str(e)}", "error")
        return redirect(url_for('listaCliente'))







# -----------------------------
# Rutas principales Para Productos
# -----------------------------

@app.route('/insertarP')
def insertarP():
    return render_template("insertarProducto.html")

@app.route('/listaP')
def listaP():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Productos")
    lista = cursor.fetchall()
    con.close()
    return render_template('listaProducto.html', listaProducto=lista)



@app.route('/insertarProducto', methods=['POST'])
def insertarProducto():
    try:
        nombre = request.form.get('txtNombrePro')
        descripcion = request.form.get('txtDescripcionPro')
        precio = request.form.get('txtPrecioPro')

        if not all([nombre, descripcion, precio]):
            flash("⚠️ Faltan campos obligatorios", "error")
            return render_template('insertarProducto.html')

        con = conectar()
        cursor = con.cursor()
        cursor.execute('''
            INSERT INTO Productos (nombre, descripcion, precio)
            VALUES (?, ?, ?)
        ''', (nombre, descripcion, precio))
        con.commit()
        con.close()

        flash("✅ Producto insertado correctamente", "success")
        return redirect(url_for('listaP'))


    except Exception as e:
        print("🔥 ERROR en el servidor:", str(e))
        flash(f"❌ Error del servidor: {str(e)}", "error")
        return render_template('crearProducto.html')
    



@app.route('/eliminarProducto/<int:idProducto>', methods=['POST'])
def eliminarProducto(idProducto):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM Productos WHERE idProducto = ?", (idProducto,))
    con.commit()
    con.close()
    return redirect(url_for('listaP'))  # O la ruta que quieras mostrar después
    


# -----------------------------
# Rutas principales Para Facturas
# -----------------------------
@app.route('/insertaF')
def insertarF():
    idFactura = request.args.get('idFactura')

    con = conectar()
    cursor = con.cursor()

    # Lista de clientes
    cursor.execute("SELECT idCliente, nombre FROM Clientes")
    lista_clientes = cursor.fetchall()

    # Lista de productos
    cursor.execute("SELECT idProducto, nombre, precio FROM Productos")
    lista_productos = cursor.fetchall()

    # Suma de precios de TODOS los productos
    cursor.execute("SELECT SUM(precio) FROM Productos")
    suma_precios = cursor.fetchone()[0] or 0  # Evita None

    # Si existe idFactura, traer el detalle de esa factura
    if idFactura:
        cursor.execute("""
            SELECT df.iddetalleFactura, p.nombre, df.cantidad, p.precio
            FROM detalleFactura df
            JOIN Productos p ON df.id_Producto = p.idProducto
            WHERE df.idFactura = %s
        """, (idFactura,))
        lista_detalleFactura = cursor.fetchall()
    else:
        lista_detalleFactura = []

    con.close()

    return render_template(
        "insertarFactura.html",
        listaClientes=lista_clientes,
        listaProductos=lista_productos,
        listadetalleFactura=lista_detalleFactura,
        sumaPrecios=suma_precios,
        idFactura=idFactura
    )




@app.route('/insertarDetalleFactura', methods=['POST'])
def insertar_detalle_factura():
    data = request.get_json()  # JSON enviado por fetch

    idFactura = data.get('idFactura')  # <-- ahora se toma del JSON
    producto = data.get('producto')
    cantidad = data.get('cantidad')

    # Validaciones
    if not idFactura or not producto or not cantidad:
        return jsonify({'msg': 'Todos los campos son obligatorios'}), 400

    try:
        con = conectar()
        cursor = con.cursor()

        cursor.execute('''
            INSERT INTO detalleFactura (id_Producto, id_Factura, cantidad)
            VALUES (?, ?, ?)
        ''', (producto, idFactura, cantidad))
        
        con.commit()
        con.close()

        return jsonify({'msg': 'Detalle insertado correctamente'}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500








@app.route('/eliminarDetalleProducto', methods=['POST'])
def eliminarDetalleProducto():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM detalleFactura")  # Quité el asterisco
    con.commit()
    con.close()
    return redirect(url_for('insertarF'))  # Ahora coincide con el nombre de la función
  # Redirige después de eliminar


@app.route("/guardarFactura", methods=["POST"])
def guardarFactura():
    data = request.get_json()

    cliente_id = int(data["cliente_id"])
    fecha = data["fecha"]
    total = float(data.get("total", 0))
    impuestos = float(data.get("impuestos", 0))

    con = conectar()
    cursor = con.cursor()

    # Insertar factura (sin detalle)
    cursor.execute("""
        INSERT INTO Facturas (idCliente, fecha, total, impuestos)
        VALUES (?, ?, ?, ?)
    """, (cliente_id, fecha, total, impuestos))
    idFactura = cursor.lastrowid

    con.commit()
    con.close()

    return jsonify({"msg": f"Factura #{idFactura} creada correctamente"})



@app.route('/listaF')
def listaF():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Facturas")
    lista = cursor.fetchall()
    con.close()
    return render_template('listaFactura.html', listaFactura=lista)





# -----------------------------
# Ejecutar app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)


