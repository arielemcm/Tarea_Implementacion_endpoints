from flask import Flask,jsonify,render_template,request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager,create_access_token,jwt_required

app = Flask(__name__)
mysql = MySQL(app)
#conexion a la BD tienda_db en mysql======
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="tienda_db"
#configurarndo JWT =======================
app.config['JWT_SECRET_KEY'] = '123'
jwt = JWTManager(app)
#============================CON JWWT /LOGIN================================
#ENDPOINT POST /login
@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username=data['username']
    password=data['password']
    if username == 'admin' and password == '123':
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    return jsonify({"error" : "Credenciales incorrectos"}),401

#============================TEST================================
@app.route('/testdb')
def test():
    cursor = mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    return "Conexion exitosa"

@app.route('/')
def inicio():
    return "Servidor flask en ejecucion"

#ENDPOINT GET/productos

#============================CATEGORIAS================================

#ENDPOINT GET /categoria
@app.route('/categorias',methods=['GET'])
@jwt_required()
def listar_categorias():
    cursor = mysql.connection.cursor()
    sql = """
        SELECT id,nombre
        FROM categoria
        """
    cursor.execute(sql)
    datos= cursor.fetchall()
    categorias=[]
    for fila in datos:
        categorias.append({"id": fila[0], "nombre": fila[1]})
    cursor.close()
    return jsonify(categorias)
#ENDPOINT GET /categorias/<id>
@app.route('/categoria/<int:id>',methods=['GET'])
def categoria_id(id):
    cursor = mysql.connection.cursor()
    sql ="""
            SELECT id,nombre
            FROM categoria
            WHERE id = %s
        """
    cursor.execute(sql,(id,))
    datos = cursor.fetchone()
    if datos is None:
        msg = {
            "mensage": "No existe la categoria!"
        }
        return jsonify(msg)
    categorias=[]
    categorias.append(
        {
            "id":datos[0],
            "nombre":datos[1]
        }
    )
    cursor.close()
    return jsonify(categorias)

#ENDPOINT POST/categorias ---- para crear una categoria en la tabla categoria--despues de producto categoria

@app.route('/categorias',methods=['POST'])
@jwt_required()
def insertar_categoria():
    # token = request.headers.get('Authorization')
    # if token != 'Bearer 13052935':
    #     return jsonify({"error" : "No esta autorizado"}),401

    return jsonify({"mensaje": "Categoria registrada con exito"}),200
    # #recuperando los datos en formato json
    # data = request.get_json()
    # nombre = data["nombre"]
    # #insertar en la tabla categoria
    # cursor = mysql.connection.cursor()
    # sql ="""
    #     INSERT INTO categoria (nombre)
    #     VALUES (%s)
    #     """
    # cursor.execute(sql,(nombre,))
    # mysql.connection.commit() #commit sirve para confirma la insercion del valor
    # cursor.close()
    # return jsonify({"mensaje": "Categoria registrada con exito"}),200

#PUT: modificar categoria
@app.route('/categorias/<int:id>',methods=['PUT'])
@jwt_required()

def modificar_categoria(id):
    
    token = request.headers.get('Authorization')
    if token != 'Bearer 13052935':
        return jsonify({"error" : "No esta autorizado"}),401
    # data = request.get_json()
    # nombre = data['nombre']
    # cursor = mysql.connection.cursor()
    # sql="""
    #     UPDATE categoria
    #     SET nombre = %s
    #     WHERE id = %s
    #     """
    # cursor.execute(sql,(nombre,id,))
    # mysql.connection.commit()
    # cursor.close()
    return jsonify({"mensaje":"Categoria modificada"}),200

#ENDPOINT DELETE
@app.route('/categorias/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_categoria(id):
    token = request.headers.get('Authorization')
    if token != 'Bearer 13052935':
        return jsonify({"error" : "No esta autorizado"}),401
    # cursor = mysql.connection.cursor()
    # sql = """
    #     SELECT id, nombre
    #     FROM categoria WHERE id = %s
    #     """
    # cursor.execute(sql, (id,))
    # datos = cursor.fetchone()
    # if datos is None:
    #     cursor.close()
    #     return jsonify({"mensaje": "La categoria no existe"}), 404
    # sql = """
    #     DELETE FROM categoria
    #     WHERE id = %s
    #     """
    # cursor.execute(sql, (id,))
    # mysql.connection.commit()
    # cursor.close()
    return jsonify({"mensaje": "Categoria eliminada"}), 200

#============================PRODCUTOS================================

#ENDPOINT GET /productos
@app.route('/productos',methods=['GET'])
def listar_productos():
    cursor = mysql.connection.cursor()
    sql = """
        SELECT id,nombre,precio,stock,categoria_id
        FROM producto
        """
    cursor.execute(sql)
    datos=cursor.fetchall()
    productos =[]
    for fila in datos:
        productos.append(
            {
                "id":fila[0],
                "nombre":fila[1],
                "precio":float(fila[2]),
                "stock":fila[3],
                "categoria_id":fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)
#ENDPOINT GET /productos/<id>
@app.route('/productos/<int:id>',methods=['GET'])
def producto_id(id):
    cursor = mysql.connection.cursor()
    sql = """SELECT id,nombre,precio,stock,categoria_id
            FROM producto
            WHERE id = %s"""
    cursor.execute(sql,(id,))
    datos = cursor.fetchone()
    if datos is None:
        msg = {
            "mensage": "No existe producto!!"
        }
        return jsonify(msg)
    productos=[]
    productos.append(
        {
            "id": datos[0],
            "nombre":datos[1],
            "precio": float(datos[2]),
            "stock":datos[3],
            "categoria_id": datos[4]
        }
    )
    cursor.close()
    return jsonify(productos)
#POST/productos crear
@app.route('/productos',methods=['POST'])
@jwt_required()
def insertar_producto():
    # token = request.headers.get('Authorization')
    # if token != 'Bearer 13052935':
    #     return jsonify({"error" : "No esta autorizado"}),401
    #rec datos
    data = request.get_json()
    nombre = data["nombre"]
    precio = float(data ["precio"])
    stock = int(data["stock"])
    categoria_id= int(data["categoria_id"])
    cursor = mysql.connection.cursor()
    sql = """
        INSERT INTO producto(nombre,precio,stock,categoria_id)
        VALUES (%s,%s,%s,%s)
        """
    cursor.execute(sql,(nombre,precio,stock,categoria_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Producto agregado correctamente -- 76. Macuchapi M. Ariel E."}),201

# PUT: para productos
@app.route('/producto/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_producto(id):
    # token = request.headers.get('Authorization')
    # if token != 'Bearer 13052935':
    #     return jsonify({"error" : "No esta autorizado"}),401

    # data = request.get_json()

    # nombre = data['nombre']
    # precio = float(data['precio'])
    # stock = int(data['stock'])
    # categoria_id = int(data['categoria_id'])

    # cursor = mysql.connection.cursor()
    # sql = """ UPDATE producto
    #     SET nombre = %s,  precio = %s,  stock = %s,categoria_id = %s
    #     WHERE id = %s
    #     """

    # cursor.execute(sql, (nombre, precio, stock, categoria_id , id,))

    # mysql.connection.commit()
    # cursor.close()
    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

#ENDPOINT DELETE/prodcuto/id
@app.route('/producto/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_prodcuto(id):
    # token = request.headers.get('Authorization')
    # if token != 'Bearer 13052935':
    #     return jsonify({"error" : "No esta autorizado"}),401

    # cursor = mysql.connection.cursor()
    # sql = """
    #     SELECT id,nombre,precio,stock,categoria_id
    #     FROM producto
    #     WHERE id = %s
    #     """
    # cursor.execute(sql, (id,))
    # datos = cursor.fetchone()
    # if datos is None:
    #     cursor.close()
    #     return jsonify({"mensaje": "El producto no existe"}),404
    # sql = """
    #     DELETE FROM producto
    #     WHERE id = %s
    #     """
    # cursor.execute(sql, (id,))
    # mysql.connection.commit()
    # cursor.close()
    return jsonify({"mensaje": "Producto eliminado"}),200

#============================EJERCICIOS CON PRODUCTOS================================

#ENDPOINT GET/productos_categoriasada
@app.route('/productos_categoria',methods=['GET'])
def productos_con_categoria():
    cursor = mysql.connection.cursor()
    sql="""
        SELECT p.id,p.nombre,p.precio,p.stock,c.nombre
        FROM producto p
        JOIN categoria c ON c.id = p.categoria_id
        """
    cursor.execute(sql)
    datos = cursor.fetchall()
    productos=[]
    for fila in datos:
        productos.append(
            {
                "id":fila[0],
                "nombre":fila[1],
                "precio":float(fila[2]),
                "stock":fila[3],
                "categoria":fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)
#ENDPOINT GET /producto/categoria/id cat
@app.route('/productos/categoria/<int:id>',methods=['GET'])
def productos_por_categoria(id):
    cursor = mysql.connection.cursor()
    sql="""
        SELECT p.id,p.nombre,p.precio,p.stock,c.nombre
        FROM producto p
        JOIN categoria c ON c.id = p.categoria_id
        WHERE c.id = %s
        """
    #se puede usar con %s and c.nombre = %s
    cursor.execute(sql,(id,)) 
    # reemplaza %s por id
    datos = cursor.fetchall()
    productos=[]
    for fila in datos:
        productos.append(
            {
                "id":fila[0],
                "nombre":fila[1],
                "precio":float(fila[2]),
                "stock":fila[3],
                "categoria":fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)
#ENDOPOINT GET/producto_mas_caro
@app.route('/producto_mas_caro',methods=['GET'])
def productos_mas_caro():
    cursor = mysql.connection.cursor()
    sql="""
        SELECT id,nombre,precio,stock,categoria_id
        FROM producto
        WHERE precio = (SELECT MAX(precio) from producto)
        """
    cursor.execute(sql)
    datos = cursor.fetchone()
    productos=[]
    productos.append(
        {
            "id":datos[0],
            "nombre":datos[1],
            "precio":float(datos[2]),
            "stock":datos[3],
            "categoria":datos[4]
        }
    )
    cursor.close()
    return jsonify(productos)
#ENDPOINT GET /prodcuto_poco_stock
@app.route('/producto_poco_stock',methods=['GET'])
def producto_poco_stock():
    cursor = mysql.connection.cursor()
    sql="""
        SELECT id,nombre,precio, stock, categoria_id
        FROM producto
        WHERE stock = (SELECT MIN(stock) from producto) 
        """
    cursor.execute(sql)
    datos = cursor.fetchone()
    productos=[]
    productos.append(
        {
            "id":datos[0],
            "nombre":datos[1],
            "precio":float(datos[2]),
            "stock":datos[3],
            "categoria":datos[4]
        }
    )
    cursor.close()
    return jsonify(productos)
#ENDPOINt GET /cantidad_producto_categoria
@app.route('/cantidad_producto_categoria',methods=['GET'])
def cantidad_producto_categoria():
    cursor = mysql.connection.cursor()
    sql = """
        SELECT c.id, c.nombre, COUNT(p.id) AS Cantidad_Producto
        FROM categoria c
        LEFT JOIN producto p ON c.id = p.categoria_id
        GROUP BY c.id,c.nombre
        """
    cursor.execute(sql)
    datos  = cursor.fetchall()
    productos=[]
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "Catidad_producto": fila[2]
            }
        )
    cursor.close()
    return jsonify(productos)
#ENDPOINT DELETE
# @app.route('/categoria/<int:id>',methods=['DELETE'])
# def elimar_categoria(id):
#     cursor = mysql.connection.cursor()
#     sql = """
#         DELETE FROM categoria
#         WHERE id = %s
#         """
#     cursor.execute(sql,(id,))
#     mysql.connection.commit()
#     cursor.close()
#     return jsonify({"mensaje":"Categoria eliminada"}),200

#============================CONEXION CON HTML================================

#conexion con html
# @app.route('/')
# def inicio():
#     return render_template("index.html")

# @app.route('/')
# def inicio():
#     return render_template("nueva_categoria.html")

# @app.route('/')
# def inicio():
#     return render_template("nueva_categoria_text.html")

# @app.route('/')
# def del_up():
#     return render_template("del_up.html")

if __name__ == '__main__':
    app.run(debug=True)


