from flask import Flask,jsonify,render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)
#conexion a la BD tienda_db en mysql
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="tienda_db"

@app.route('/testdb')
def test():
    cursor = mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    return "Conexion exitosa"

# @app.route('/')
# def inicio():
#     return "Servidor flask en ejecucion"

#ENDPOINT GET /categoria
@app.route('/categorias',methods=['GET'])
def listar_categorias():
    cursor = mysql.connection.cursor()
    sql = "SELECT id,nombre FROM categoria"
    cursor.execute(sql)
    datos= cursor.fetchall()
    categorias=[]
    for fila in datos:
        categorias.append({"id": fila[0], "nombre": fila[1]})
    cursor.close()
    return jsonify(categorias)

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

#ENDPOINT GET /categorias/<id>
@app.route('/categorias/<int:id>',methods=['GET'])
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
#ENDPOINT GET/productos
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
#conexion con html
@app.route('/')
def inicio():
    return render_template("index.html")
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
if __name__ == '__main__':
    app.run(debug=True)


