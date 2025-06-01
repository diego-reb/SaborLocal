from flask import Flask, render_template, request, redirect, url_for, flash,current_app,  session, jsonify,  make_response, send_file
import requests, io
from functools import wraps
from requests.auth import HTTPBasicAuth
from src.config import DevelopmentConfig
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Usuario
from models.Productos import Producto
from models.tipousuario import TipoUsuario
from models.Vendedor import Vendedor
from models.Administrador import Administrador
from models.Pago import Pago
from models.Clientes import Clientes
from models.Direccion import Direccion
from models.Colonia import Colonia
from models.CP import CodigoPostal
from models.Alcaldia import Alcaldia
from models.ProductoPedido import ProductoPedido
from src.conexion import conexion
from functools import wraps
from flask_mail import Message
from extension import mail
import os, json
from decimal import Decimal
import base64


app = Flask(__name__)
app.secret_key= 'clave_secreta'
app.config.from_object(DevelopmentConfig)
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'dzgarcia10@gmail.com'
app.config['MAIL_PASSWORD'] = 'bpnw dwmr ispt jmvv'
app.config['MAIL_DEFAULT_SENDER'] = 'dzgarcia10@gmail.com'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/SaborLocal' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db.init_app(app)
mail.init_app(app)
#----------------------------------------------------------------------
#--------------------------Comprobacion con la base de datos----------------

@app.route("/db")
def bd():
    conn=conexion()
    if not conn:
        return "No hay conexión con la base de datos."
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        resultado = cur.fetchone()
        cur.close()
        return f"Conexión exitosa. Resultado de prueba: {resultado[0]}"
    except Exception as e:
       return f"Error al ejecutar la consulta de prueba: {e}"
#-------------------------------------------------------
#---------------------------Pagina principal-------------
@app.route("/")
@nocache
def sesion():
    return render_template('sesion.html')
#----------------------------------------------------------
@app.route ("/sesion")
@nocache
def Main ():
    sesion_activa = 'cliente_id' in session
    return render_template('index.html', sesion_activa=sesion_activa)
#--------------------------login--------------------------- 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        cliente = Clientes.query.filter_by(correo=correo).first()

        if cliente and check_password_hash(cliente.contraseña, contraseña):
            session['cliente_id'] = cliente.id_cliente
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('Main'))  
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('login'))  

    return render_template('login.html')
@app.route("/logout")
def logout():
    session.clear() 
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('login'))

#---------------------------------------------------------------
#-----------------------------login administrador----------------------------------
@app.route ('/LoginAdmin', methods=['GET','POST'])
@nocache
def loginadmin():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request. form ['contraseña']
        administrador = Administrador.query.filter_by(correo=correo).first()
        if administrador and check_password_hash(administrador.contraseña,contraseña):
            session['administrador_id'] = administrador.id_administrador 
            flash ("Inicio de sesion exitorso como administrador")
            return redirect(url_for('inadmin'))
        else:
            flash ("correo o contraseña incorrectos")
            return redirect(url_for('loginadmin'))

    return render_template('LoginAdm.html')
@app.route("/logout_admin")
def logout_admin():
    session.clear()
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('loginadmin'))

@app.route('/verificar-sesion-admin')
def verificar_sesion_admin():
    activa = 'admin_id' in session
    return jsonify({'activa': activa})

@app.route('/cacheadmin')
@nocache
def cacheadmin():
    if 'administrador_id' not in session:
        flash("Debes iniciar sesión como administrador", "warning")
        return redirect(url_for('loginadmin'))
    
    return render_template('panel_admin.html')



#---------------------------------------------------------------
#-----------------------------Login vendedor----------------------------------
@app.route('/LoginVen', methods=['GET', 'POST'])
def loginven():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        vendedor = Vendedor.query.filter_by(correo=correo).first()

        if vendedor and check_password_hash(vendedor.contraseña, contraseña):
            session['vendedor_id'] = vendedor.vendedor_id  # Guardar el ID en la sesión
            flash("Inicio de sesión exitoso como vendedor", "success")
            return redirect(url_for('Ven'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('loginven'))

    return render_template('LoginVen.html')
@app.route('/logoutV')
def logoutV():
    session.clear()  # Elimina todos los datos de sesión
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for('loginven'))  # Redirige al login del vendedor

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'vendedor_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for('loginven'))
        return f(*args, **kwargs)
    return decorada
#-----------------------------Fin Login vendedor----------------------------------

#-------------------Registro------------------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        telefono = request.form['telefono']
        
        contraseña_hash = generate_password_hash(contraseña)
        nuevo_usuario = Clientes( nombre=nombre,correo=correo,contraseña=contraseña_hash,telefono=telefono)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registro.html')

#-----------------------------------Fin registro----------------------


@app.route("/RegistroVen", methods=["GET", "POST"])
def regve():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        # Verificar si ya existe un vendedor con ese correo
        vendedor_existente = Vendedor.query.filter_by(correo=correo).first()
        if vendedor_existente:
            flash("Este correo ya está registrado. Intenta con otro.", "warning")
            return redirect(url_for("regve"))

        # Crear nuevo vendedor con contraseña hasheada
        nuevo_vendedor = Vendedor(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            contraseña=generate_password_hash(contraseña)
        )

        # Guardar en la base de datos
        db.session.add(nuevo_vendedor)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("loginven"))

    return render_template("RegistroVen.html")
#-----------------------------config----------------------------------
@app.route("/config")
def menu():
    return render_template('config.html')
#---------------------------fin config--------------------------------
#-------------------------------------- agregar producto--------------------------
@app.route('/AP', methods=['GET', 'POST'])
@nocache
@login_requerido
def agregar_producto():
    categorias = obtener_categorias()

    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        descripcion = request.form['descripcion']
        precio_str = request.form['precio'].replace(',', '.')
        precio = float(precio_str)
        id_cat = request.form.get("categoria")  

        print("Datos recibidos:", nombre_producto, descripcion, precio, id_cat)

        imagen = request.files['imagen']
        imagen_binaria = imagen.read() if imagen else None

        producto = Producto(
            nombre=nombre_producto,
            descripcion=descripcion,
            precio=precio,
            id_cat=id_cat,
            imagen=imagen_binaria
        )
        producto.guardar()

        return redirect(url_for('Catalogo_vendedor'))

    productos = Producto.obtener_todos()
    return render_template('aproducto.html', categorias=categorias, productos=productos)


def obtener_categorias():
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cat, nombre_categoria FROM categoria")
        return cursor.fetchall() 
    except Exception as e:
        print(f"Error al obtener categorías: {e}")
        return []
    finally:
        if conn:
            conn.close()
           

@app.route('/imagen_producto/<int:id_pro>')
def imagen_producto(id_pro):
    producto = Producto.obtener_por_id(id_pro)  
    if producto and producto.imagen:
        return send_file(io.BytesIO(producto.imagen), mimetype='image/jpeg') 
    else:
        return send_file('static/Img/default.png', mimetype='image/png')

#--------------------------------------------fin agregar producto-----------------------------
#--------------------------------------------Carrito------------------------------------------
@app.route("/C")
@nocache
def Carrito():
    return render_template ('carrito.html')
@app.route('/agregar_producto_carrito', methods=['POST'])
def agregar_producto_carrito():
    if 'cliente_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')
    cantidad = data.get('cantidad')
    subtotal = precio * cantidad
    cliente_id = session['cliente_id']

    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ProductoPedido (nombre, precio_unitario, cantidad, subtotal, cliente_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, precio, cantidad, subtotal, cliente_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Producto guardado en base de datos'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Error al guardar en la base de datos'}), 500

#--------------------------------------------fin carrito--------------------------------------
#--------------------------------------------catalogo vendedor-------------------------------
@app.route("/CV")
@nocache
@login_requerido
def Catalogo_vendedor():
    productos = Producto.obtener_todos()
    return render_template('catalogo_vendedor.html', productos=productos)

@app.route("/producto/eliminar/<int:id_pro>", methods=["POST"], endpoint="eliminar_producto")
def eliminar_producto(id_pro):
    Producto.eliminar(id_pro)
    return redirect(url_for('Catalogo_vendedor'))

@app.route("/producto/editar/<int:id_pro>", methods=["GET", "POST"], endpoint="editar_producto")
def editar_producto(id_pro):
    producto = Producto.obtener_por_id(id_pro)

    if not producto:
        return "Producto no encontrado", 404

    categorias = obtener_categorias()

    if request.method == "POST":
        nombre_producto = request.form.get("nombre_producto")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio").replace(',', '.')  
        id_cat = request.form.get("categoria")

        imagen_binaria = None
        if 'imagen' in request.files:
            imagen_archivo = request.files['imagen']
            if imagen_archivo and imagen_archivo.filename != '':
                imagen_binaria = imagen_archivo.read()  

        Producto.actualizar(id_pro, nombre_producto, descripcion, precio, id_cat, imagen_binaria)

        return redirect(url_for('Catalogo_vendedor'))

    return render_template("editproductos.html", producto=producto, categorias=categorias)


#-------------------------------------------fin catalogo vendedor----------------------------
#------------------------------------------- catalogo----------------------------
@app.route("/CA")
def Catalogo():
    productos = Producto.obtener_todos()
    return render_template ('catalogo.html', productos=productos)
#-------------------------------------------fin catalogo----------------------------
#-------------------------------------------editar productos----------------------------
@app.route("/EP") 
def Edit_productos():
    id_producto = request.args.get("id_producto", default=1, type=int)  
    producto = Producto.obtener_por_id(id_producto)

    if not producto:
        return "Producto no encontrado", 404

    return render_template("editproductos.html", producto=producto)


def obtener_categorias():
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cat, nombre_categoria FROM categoria")
        return cursor.fetchall() 
    except Exception as e:
        print(f"Error al obtener categorías: {e}")
        return []
    finally:
        if conn:
            conn.close()

@app.route("/producto/edita/<int:id_pro>", methods=["GET", "POST"])
def editar_producto_vendedor(id_pro):
    producto = Producto.obtener_por_id(id_pro)
    
    if not producto:
        return "Producto no encontrado", 404 

    
    categorias = obtener_categorias()
    print(categorias)  

    if request.method == "POST":
        print("FORM DATA:", request.form)  # Verifica si llega correctamente
        nombre_producto = request.form.get("nombre_producto")  # Usamos get() por seguridad
        descripcion = request.form.get("descripcion")
        precio = float(request.form['precio'])

        id_cat = request.form.get("categoria")
        imagen = None
        if 'imagen' in request.files:
            imagen_archivo = request.files['imagen']
            if imagen_archivo.filename != '':
                imagen = guardar_imagen(imagen_archivo)

        Producto.actualizar(id_pro, nombre_producto, descripcion, precio, id_cat, imagen)
        return redirect(url_for('Catalogo_vendedor'))

    return render_template("editproductos.html", producto=producto, categorias=categorias)
def guardar_imagen(archivo):
    filename = secure_filename(archivo.filename)
    filepath = os.path.join('static/Img', filename)
    archivo.save(filepath)
    return filename
@staticmethod
def actualizar(id_pro, nombre_producto, descripcion, precio, id_cat, imagen=None):
    try:
        conn = conexion()
        cursor = conn.cursor()
        if imagen:
            cursor.execute("""
                UPDATE producto
                SET nombre_producto = %s, descripcion = %s, precio = %s, id_cat = %s, imagen = %s
                WHERE id_pro = %s
            """, (nombre_producto, descripcion, precio, id_cat, imagen, id_pro))  # Asegúrate de usar nombre_producto
        else:
            cursor.execute("""
                UPDATE producto
                SET nombre_producto = %s, descripcion = %s, precio = %s, id_cat = %s
                WHERE id_pro = %s
            """, (nombre_producto, descripcion, precio, id_cat, id_pro))  # Asegúrate de usar nombre_producto

        conn.commit()
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
    finally:
        if conn:
            conn.close()



#-------------------------------------------fin editar productos----------------------------
#-------------------------------------------pedidos----------------------------
@app.route("/P")
def pedidos():
    return render_template ('pedidos.html')
#-------------------------------------------fin pedidos----------------------------
#-------------------------------------------promociones----------------------------
@app.route("/PC")
def promociones():
    return render_template ('promociones.html')
#-------------------------------------------fin promociones----------------------------
#-------------------------------------------vendedor----------------------------
@app.route("/V")
@nocache
@login_requerido
def Ven():
    return render_template ('Vendedor.html')
#-------------------------------------------fin vendedor----------------------------
#-------------------------------------------pago----------------------------
@app.route("/pago", methods=["GET", "POST"])
def pago():
    if request.method == "POST":
        direccion = request.form['direccion']
        colonia = request.form['colonia']
        ciudad = request.form['ciudad']
        codigo_postal = request.form['cp']
        horario_entrega = request.form.get('entrega')
        notas_adicionales = request.form.get('nota')
        nombre = request.form['nombre']
        correo = request.form['correo']
        metodo_pago = request.form['pago']
        fecha_entrega = request.form['fecha']
        fecha_expiracion = request.form.get('fecha_expiracion') if metodo_pago == 'tarjeta' else None
        numero_tarjeta = request.form.get('numero_tarjeta') if metodo_pago == 'tarjeta' else None
        cvv = request.form.get('cvv') if metodo_pago == 'tarjeta' else None

        # Crear el nuevo pago
        nuevo_pago = Pago(
            direccion=direccion,
            colonia=colonia,
            ciudad=ciudad,
            codigo_postal=codigo_postal,
            horario_entrega=horario_entrega,
            notas_adicionales=notas_adicionales,
            nombre=nombre,
            correo=correo,
            metodo_pago=metodo_pago,
            fecha_entrega=fecha_entrega,
            numero_tarjeta=numero_tarjeta,
            cvv=cvv,
            fecha_expiracion=fecha_expiracion
        )

        db.session.add(nuevo_pago)
        db.session.flush()  
        carrito_json = request.form["carrito"]
        carrito = json.loads(carrito_json)

        for producto in carrito:
            nuevo_producto = ProductoPedido(
            id_pago=nuevo_pago.id,
            nombre_producto=producto["nombre_producto"],
            precio_unitario=producto["precio"],
            cantidad=producto["cantidad"],
            subtotal=float(producto["precio"]) * int(producto["cantidad"])
            )
            db.session.add(nuevo_producto)
            db.session.commit()

        # Enviar correo de confirmación
        enviar_correo_usuario(
            nombre=nombre,
            correo=correo,
            direccion=direccion,
            colonia=colonia,
            ciudad=ciudad,
            codigo_postal=codigo_postal,
            metodo_pago=metodo_pago,
            fecha_entrega=fecha_entrega
        )

        flash("¡Pago procesado correctamente! Se ha enviado un correo de confirmación.", "success")
        return redirect(url_for('Catalogo', pago_exitoso=True))

    # GET: Cargar colonias
    conn = conexion()
    cur = conn.cursor()
    cur.execute("SELECT colonia FROM colonia")
    colonias = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    return render_template('pago.html', colonias=colonias)

def enviar_correo_usuario(nombre, correo, direccion, colonia, ciudad, codigo_postal, metodo_pago, fecha_entrega):
    
    mensaje = Message(
        subject="Confirmación de Compra - Sabor Local",
        recipients=[correo],
        body=f"""
        Hola {nombre},

        Gracias por realizar tu compra con nosotros. Aquí están los detalles de tu pedido:

        Dirección de entrega:
        Calle: {direccion}
        Colonia: {colonia}
        Ciudad: {ciudad}
        Código Postal: {codigo_postal}

        Método de pago: {metodo_pago}
        Fecha de entrega preferida: {fecha_entrega}

        ¡Esperamos que disfrutes de tus productos!

        Saludos,
        El equipo de Sabor Local
        """
    )
    
    try:
        mail.send(mensaje)
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

@app.route("/finalizar_pago", methods=["POST"])
def finalizar_pago():
    # Obtener los datos del frontend
    datos = request.get_json()
    nombre = datos.get("nombre")
    correo = datos.get("correo")
    direccion = datos.get("direccion")
    colonia = datos.get("colonia")
    ciudad = datos.get("ciudad")
    codigo_postal = datos.get("codigo_postal")
    metodo_pago = datos.get("metodo_pago")
    fecha_entrega = datos.get("fecha_entrega")
    
    
    # Llamar a la función para enviar el correo
    enviar_correo_usuario(
        nombre=nombre,
        correo=correo,
        direccion=direccion,
        colonia=colonia,
        ciudad=ciudad,
        codigo_postal=codigo_postal,
        metodo_pago=metodo_pago,
        fecha_entrega=fecha_entrega,
        
    )
    
    return jsonify({"success": True})

#-------------------------------------------fin pago----------------------------
#-------------------------------------------administrar clientes----------------------------

@app.route("/AD")
@nocache
def aclientes():
    clientes = Clientes.query.all()
    return render_template('admclientes.html', clientes=clientes)

@app.route('/eliminar_cliente/<int:id_cliente>', methods=['POST'])
def eliminar_cliente(id_cliente):
    print(f"Solicitud para eliminar cliente con ID: {id_cliente}")
    cliente = Clientes.query.get(id_cliente)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        print("Cliente eliminado de la base de datos")
        return jsonify({"success": True, "message": "Cliente eliminado correctamente"})
    else:
        print("Cliente no encontrado")
        return jsonify({"success": False, "message": "Cliente no encontrado"}), 404

@app.route('/toggle_estado/<int:id_cliente>', methods=['POST'])
def toggle_estado(id_cliente):
    cliente = Clientes.query.get(id_cliente)
    if cliente:
        cliente.activo = not cliente.activo
        db.session.commit()
        return jsonify({'success': True, 'nuevo_estado': cliente.activo})
    return jsonify({'success': False}), 404

@app.route('/modificar_cliente/<int:id>', methods=['POST'])
def modificar_cliente(id):
    data = request.json
    cliente = Clientes.query.get(id)
    
    if not cliente:
        return jsonify(success=False, message="Cliente no encontrado")

    cliente.nombre = data['nombre']
    cliente.telefono = data['telefono']
    cliente.correo = data['correo']

    if 'contrasena' in data and data['contrasena'].strip() != "":
        hash_contraseña = generate_password_hash(data['contrasena'])
        cliente.contraseña = hash_contraseña

    db.session.commit()
    return jsonify(success=True)

# ✅ NUEVA RUTA PARA AGREGAR CLIENTES
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    data = request.json

    if not all(k in data for k in ('nombre', 'telefono', 'correo', 'contrasena')):
        return jsonify(success=False, message="Faltan campos obligatorios"), 400

    nuevo_cliente = Clientes(
        nombre=data['nombre'],
        telefono=data['telefono'],
        correo=data['correo'],
        contraseña=generate_password_hash(data['contrasena']),
        activo=True  # O False, según tu lógica
    )

    db.session.add(nuevo_cliente)
    db.session.commit()

    return jsonify(success=True, message="Cliente agregado correctamente")


#-------------------------------------------fin administrar clientes----------------------------
#-------------------------------------------administrar vendedores----------------------------
@app.route ("/ADV")
def avendedores():
    vendedores=Vendedor.query.all( )
    return render_template ('admvendedores.html', vendedores=vendedores)
from werkzeug.security import generate_password_hash

@app.route('/registrar_vendedor', methods=['POST'])
def registrar_vendedor():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        telefono = data.get('telefono')
        correo = data.get('correo')
        contrasena = data.get('contraseña')

        if not all([nombre, telefono, correo, contrasena]):
            return jsonify({"success": False, "message": "Campos incompletos"}), 400

        hashed = generate_password_hash(contrasena)

        nuevo_vendedor = Vendedor(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            contraseña=hashed  # ← usa la ñ
        )
        db.session.add(nuevo_vendedor)
        db.session.commit()

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error al registrar vendedor: {e}")
        return jsonify({"success": False, "message": "Error interno"}), 500

@app.route('/eliminar_vendedor/<int:vendedor_id>', methods=['POST'])
def eliminar_vendedor(vendedor_id):
    print(f"Solicitud para eliminar vendedores con ID: {vendedor_id}")
    vendedor = Vendedor.query.get(vendedor_id)
    if vendedor:
        db.session.delete(vendedor)
        db.session.commit()
        print("Vendedor eliminado de la base de datos")
        return jsonify({"success": True, "message": "Vendedor eliminado correctamente"})
    else:
        print("Vendedor no encontrado")
        return jsonify({"success": False, "message": "Vendedor no encontrado"}), 404


@app.route("/toggle_estadov/<int:vendedor_id>", methods=["POST"])
def toggle_estadov(vendedor_id):
    vendedor = Vendedor.query.get(vendedor_id)
    if vendedor:
        # Cambiar el estado activo/inactivo
        vendedor.activo = not vendedor.activo
        db.session.commit()
        return jsonify({'success': True, 'nuevo_estado': vendedor.activo})
    return jsonify({'success': False}), 404

@app.route('/modificar_vendedor/<int:id>', methods=['POST'])
def modificar_vendedor(id):
    data = request.json
    vendedor = Vendedor.query.get(id)
    if vendedor:
        vendedor.nombre = data['nombre']
        vendedor.telefono = data['telefono']
        vendedor.correo = data['correo']
        
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404



#-------------------------------------------fin administrar vendedores----------------------------
#-------------------------------------------devolucion de producto----------------------------
@app.route ("/DP")
def devolucion():
    return render_template ('devprodu.html')
#-------------------------------------------fin devolucion de producto----------------------------
#-------------------------------------------direccion----------------------------
@app.route("/Direccion", methods=['GET', 'POST'])
def direccion():
        if request.method == 'POST':
            print(request.form)  # Imprime los datos del formulario
            nueva_direccion = Direccion(
                calle=request.form['calle'],
                id_col=request.form['colonia'],
                id_al=request.form['alcaldia'],
                lote=request.form['lote'],
                mz=request.form['mz'],
                id_cp=request.form['cp'],
                numero=request.form['no_int'],
                num_ext=request.form['numero'],
                referencias=request.form['referencias']
            )
            db.session.add(nueva_direccion)
            db.session.commit()
            return redirect('/Direccion')
  
        codigos_postales = CodigoPostal.query.all() 
        colonias = Colonia.query.all()
        alcaldias = Alcaldia.query.all()
        return render_template('direccion.html', colonias=colonias, alcaldias=alcaldias, codigos_postales=codigos_postales)

#-------------------------------------------fin direccion----------------------------
#-------------------------------------------editar metodo de pago----------------------------
@app.route ("/EP")
def epago():
    return render_template ('edpago.html')
#-------------------------------------------fin editar pago----------------------------
#-------------------------------------------inicio de administrador----------------------------
@app.route ("/IA")
@nocache
def inadmin():
    print("SESION ACTUAL:", session)
    if 'administrador_id' not in session:
        flash("Debes iniciar sesión como administrador", "warning")
        return redirect(url_for('loginadmin'))

    return render_template ('inadmin.html')
#-------------------------------------------fin inicio de administrador----------------------------
#-------------------------------------------Motivos de la devolucion----------------------------
@app.route ("/MT")
def motivdevo():
    return render_template ('motivdevo.html')
#-------------------------------------------fin motivos de la devolucion----------------------------

#-------------------------------------------Gestor Administrador----------------------------

@app.route("/VA")
@nocache
def vad():
    admin = Administrador.query.all()
    return render_template('visadmin.html', administradores=admin)

@app.route('/eliminar_admin/<int:admin_id>', methods=['POST'])
def eliminar_admin(admin_id):
    admin = Administrador.query.get(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/toggle_estado_admin/<int:admin_id>', methods=['POST'])
def toggle_estado_admin(admin_id):
    admin = Administrador.query.get(admin_id)
    if admin:
        admin.activo = not admin.activo
        db.session.commit()
        return jsonify({'success': True, 'nuevo_estado': admin.activo})
    return jsonify({'success': False}), 404

@app.route("/registrar_admin", methods=['POST'])
def registrar_admin():
    nombre = request.form['nombre']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    hash_contraseña = generate_password_hash(contraseña)
    nuevo_admin = Administrador(nombre=nombre, correo=correo, contraseña=hash_contraseña, activo=True)
    
    # Agregar a la base de datos
    db.session.add(nuevo_admin)
    db.session.commit()

    return redirect('/VA') 

@app.route('/modificar_administrador/<int:id_administrador>', methods=['POST'])
def modificar_administrador(id_administrador):
    data = request.json
    admin_a_modificar = Administrador.query.get(id_administrador)
    if admin_a_modificar:
        admin_a_modificar.nombre = data.get('nombre', admin_a_modificar.nombre)
        admin_a_modificar.correo = data.get('correo', admin_a_modificar.correo)
        
        nueva_contrasena = data.get('contrasena')
        if nueva_contrasena:
            admin_a_modificar.contraseña = nueva_contrasena 
        
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404


#-------------------------------------------Fin Gestor----------------------------
@app.route("/ADP")
def aproductos():
    productos = Producto.obtener_todos()
    categorias = Producto.obtener_categorias()
    return render_template("admproductos.html", productos=productos, categorias=categorias) # Asegúrate de que "productos-html" sea el nombre correcto de tu plantilla

@app.route("/Apt", methods=["POST"])
def agregar_productoadmin():
    try:
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        precio = float(request.form["precio"])
        id_cat = (request.form["categoria"]) 
        imagen_file = request.files.get("imagen")
        imagen_bytes = None

        if imagen_file and imagen_file.filename != "":
            imagen_bytes = imagen_file.read()

        nuevo = Producto(nombre=nombre, descripcion=descripcion, precio=precio, id_cat=id_cat, imagen=imagen_bytes)
        if nuevo.guardar():
            return jsonify({"success": True, "message": "Producto agregado correctamente."})
        else:
            return jsonify({"success": False, "message": "Error al guardar el producto en la base de datos."}), 500
    except Exception as e:
        print(f"Error en agregar_productoadmin: {e}")
        return jsonify({"success": False, "message": f"Error interno del servidor: {e}"}), 500


@app.route("/productoa/editar", methods=["POST"])
def editar_productoa():
    try:
        id_pro = int(request.form["id_pro"])
        nombre_producto = request.form["nombre"]  # Cambia a nombre_producto
        descripcion = request.form["descripcion"]
        precio = float(request.form["precio"])
        id_cat = request.form["categoria"]

        imagen_file = request.files.get("imagen")
        imagen_bytes = None
        if imagen_file and imagen_file.filename != "":
            imagen_bytes = imagen_file.read()

        # Cambia aquí el nombre del argumento
        if Producto.actualizar(id_pro, nombre_producto, descripcion, precio, id_cat, imagen_bytes):
            return jsonify({"success": True, "message": "Producto actualizado correctamente."})
        else:
            return jsonify({"success": False, "message": "Error al actualizar el producto en la base de datos."}), 500
    except Exception as e:
        print(f"Error en editar_productoa: {e}")
        return jsonify({"success": False, "message": f"Error interno del servidor: {e}"}), 500

@app.route('/productoa/eliminar/<int:id_pro>', methods=['POST'])
def eliminar_productoa(id_pro):
    try:
        if Producto.eliminar(id_pro):
            return jsonify({"success": True, "message": f"Producto con ID {id_pro} eliminado correctamente."})
        else:
            return jsonify({"success": False, "message": "Error al eliminar el producto de la base de datos."}), 500
    except Exception as e:
        print(f"Error en eliminar_productoa: {e}")
        return jsonify({"success": False, "message": f"Error interno del servidor: {e}"}), 500


if __name__=='__main__':
    app.config.from_object(DevelopmentConfig)

    app.run()

