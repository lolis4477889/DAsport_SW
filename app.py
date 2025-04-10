from flask import Flask, redirect, render_template, request,session, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename


app = Flask (_name_)

# Configuración para almacenar imágenes
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.secret_key="david"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login"
    )

# Función para verificar extensiones de archivos permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


#Funcion para el login

@app.route("/acceso-login", methods= ["GET","POST"])
def login():

    if request.method == "POST" and "txtCorreo" in request.form and "txtPassword":
        _correo = request.form["txtCorreo"]
        _contraseña = request.form["txtPassword"]
        conn = get_db_connection #llamamos a la conexion de base de datos 
        cursor = conn.cursor(account)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s, password = %s", (_correo, _contraseña),)
        account = cursor.fechone()

        if account: #verificar que los datos del admin sean correctos 
            session["logueado"]=True
            session["id"]= account

            return render_template("admin.html")
        else:

            return render_template("index.html")
        
        #cursor.close()
        #conn.close()
    

    return render_template("admin.html")


@app.route("/seleccionar tabla", methods=["GET", "POST"])
def agregar():

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    miresultado = cursor.fetchall()
     # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in miresultado:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    conn.close()
    return render_template("admin.html", dato=insertObject)


#clase para agregar los productos
@app.route("/agregar_productos", methods = ["POST"])
def productos():

    _Producto = request.form["nombre_producto"]
    __Cantidad = int(request.form["cantidad_producto"])
    _Descripcion = request.form["descripcion"]

     # Manejo de la imagen
    if "imagen" in request.files:
        file = request.files["imagen"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            filename = "default.jpg"  # Imagen por defecto si no se sube ninguna
    else:
        filename = "default.jpg"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre_producto, cantidad_producto, descripcion, imagen) VALUES (%s, %s, %s, %s, %s)", (_Producto, __Cantidad, _Descripcion, filename))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("admin.html", "usuarios.html"))

#clase para actualizar los productos
@app.route ("/actualizar productos/<string:id>", methods=["POST"])
def actualizar(id):
    _Producto = request.form["nombre_producto"]
    __Cantidad = int(request.form["cantidad_producto"])
    _Descripcion = request.form["descripcion"]

    conn = get_db_connection()
    cursor = conn.cursor()

        # Verificar si se subió una nueva imagen
    if "imagen" in request.files:
        file = request.files["imagen"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Actualizar el producto con la nueva imagen
            cursor.execute("UPDATE productos SET nombre_producto=%s, cantidad_producto=%s, descripcion=%s, imagen=%s WHERE id=%s",
                           (Producto,_Cantidad, _Descripcion, filename, id))
        else:
            # Si no se sube una nueva imagen, se mantiene la actual
            cursor.execute("UPDATE productos SET nombre_producto=%s, cantidad_producto=%s, descripcion=%s WHERE id=%s",
                           (_Producto, __Cantidad, _Descripcion, id))
    else:
        cursor.execute("UPDATE productos SET nombre_producto=%s, cantidad_producto=%s, descripcion=%s WHERE id=%s",
                       (_Producto, __Cantidad, _Descripcion, id))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("admin.html", "usuarios.html"))

@app.route ("/delete/<int:id>")
def eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("admin.html"))

app.py
