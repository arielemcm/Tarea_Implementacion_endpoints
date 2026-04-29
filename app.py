from flask import Flask,jsonify,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)
#conexion a la BD tienda_db en mysql
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="tienda_db"
#============================TEST================================
@app.route('/testdb')
def test():
    cursor = mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    return "Conexion exitosa"

# @app.route('/')
# def inicio():
#     return "Servidor flask en ejecucion"

#ENDPOINT GET/productos

#============================CATEGORIAS================================

#ENDPOINT GET /categoria
@app.route('/categorias',methods=['GET'])
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
def insertar_categoria():
    #recuperando los datos en formato json
    data = request.get_json()
    nombre = data["nombre"]

    #insertar en la tabla categoria
    cursor = mysql.connection.cursor()
    sql ="""
        INSERT INTO categoria (nombre)
        VALUES (%s)
        """
    cursor.execute(sql,(nombre,))
    mysql.connection.commit() #commit sirve para confirma la insercion del valor
    cursor.close()
    return jsonify({"Mensaje": "Categoria registrada con exito"}),200
#PUT: modificar categoria
@app.route('/categorias/<int:id>',methods=['PUT'])
def modificar_categoria(id):
    data = request.get_json()
    nombre = data['nombre']
    cursor = mysql.connection.cursor()
    sql="""
        UPDATE categoria
        SET nombre = %s
        WHERE id = %s
        """
    cursor.execute(sql,(nombre,id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Categoria modificada"}),200

#ENDPOINT DELETE
@app.route('/categoria/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    cursor = mysql.connection.cursor()
    sql = """
        SELECT id, nombre
        FROM categoria WHERE id = %s
        """
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if datos is None:
        cursor.close()
        return jsonify({"mensaje": "La categoria no existe"}), 404
    sql = """
        DELETE FROM categoria
        WHERE id = %s
        """
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
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
def insertar_producto():
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
    return jsonify({"mensaje":"Producto agregado correctamente"}),201

# PUT: para productos
@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):

    data = request.get_json()

    nombre = data['nombre']
    precio = float(data['precio'])
    stock = int(data['stock'])
    categoria_id = int(data['categoria_id'])

    cursor = mysql.connection.cursor()
    sql = """ UPDATE producto
        SET nombre = %s,  precio = %s,  stock = %s,categoria_id = %s
        WHERE id = %s
        """

    cursor.execute(sql, (nombre, precio, stock, categoria_id , id,))

    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

#ENDPOINT DELETE/prodcuto/id
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_prodcuto(id):
    cursor = mysql.connection.cursor()
    sql = """
        SELECT id,nombre,precio,stock,categoria_id
        FROM producto
        WHERE id = %s
        """
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if datos is None:
        cursor.close()
        return jsonify({"mensaje": "El producto no existe"}),404
    sql = """
        DELETE FROM producto
        WHERE id = %s
        """
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
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
@app.route('/')
def inicio():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)


