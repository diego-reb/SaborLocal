from src.conexion import conexion
from extension import db
from werkzeug.utils import secure_filename
import os
import base64
from decimal import Decimal


class Producto:
    __tablename__ = 'producto'

    def __init__(self, id_pro=None, nombre=None, descripcion=None, precio=None, id_cat=None, imagen=None, categoria=None):
        self.id_pro = id_pro
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = Decimal(str(precio))
        self.id_cat = id_cat
        self.imagen = imagen
        self.categoria = categoria  

    def guardar(self):
        try:
            conn = conexion()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO producto (nombre_producto, descripcion, precio, id_cat, imagen)
                VALUES (%s, %s, %s, %s, %s)
            """, (self.nombre, self.descripcion, self.precio, self.id_cat, self.imagen))
            conn.commit()
            return True  # ✅ Agrega esto
        except Exception as e:
            print(f"Error al guardar el producto: {e}")
            return False  # ✅ Agrega esto
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtener_todos():
        productos = []
        conn = None
        try:
            conn = conexion()
            cursor = conn.cursor()
            query = """
                SELECT p.id_pro, p.Nombre_Producto, p.Descripcion, p.Precio, p.id_cat, p.imagen, c.nombre_categoria
                FROM Producto p
                JOIN Categoria c ON p.id_cat = c.id_cat
                ORDER BY p.id_pro ASC
            """
            cursor.execute(query)
            filas = cursor.fetchall()

            for fila in filas:
                imagen_codificada = None
                if fila[5]: 
                    imagen_codificada = base64.b64encode(fila[5]).decode('utf-8')  

                producto = Producto(
                    id_pro=int(fila[0]),  
                    nombre=fila[1],
                    descripcion=fila[2],
                    precio=fila[3],
                    id_cat=fila[4],
                    imagen=imagen_codificada  
                )
                producto.categoria = fila[6]
                productos.append(producto)

            return productos
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar(id_pro):
        try:
            conn = conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM producto WHERE id_pro = %s", (id_pro,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def guardar_imagen(archivo):
        filename = secure_filename(archivo.filename)
        filepath = os.path.join('static/Img', filename)
        archivo.save(filepath)
        print(f"Imagen guardada como: {filename}")  # Verifica que el nombre del archivo sea correcto
        return filename


    @staticmethod
    def obtener_por_id(id_pro):
        try:
            conn = conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_pro, nombre_producto, descripcion, precio, id_cat, imagen FROM producto WHERE id_pro = %s", (id_pro,))
            row = cursor.fetchone()
            if row:
                print("Producto encontrado:", row)  # DEBUG
                return Producto(*row)
            return None
        except Exception as e:
            print(f"Error al obtener producto por ID: {e}")
            return None
        finally:
            if conn:
                conn.close()


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
                """, (nombre_producto, descripcion, precio, id_cat, imagen, id_pro))
            else:
                cursor.execute("""
                    UPDATE producto
                    SET nombre_producto = %s, descripcion = %s, precio = %s, id_cat = %s
                    WHERE id_pro = %s
                """, (nombre_producto, descripcion, precio, id_cat, id_pro))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False
        finally:
            if conn:
                conn.close()

    
# Puedes poner esto en models/Categoria.py o en Productos.py si no tienes un archivo aparte
    @staticmethod
    def obtener_categorias():
        categorias = []
        conn = None
        try:
            conn = conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_cat, nombre_categoria FROM Categoria ORDER BY nombre_categoria ASC")
            filas = cursor.fetchall()
            for fila in filas:
                categorias.append({'id': fila[0], 'nombre': fila[1]})
            return categorias
        except Exception as e:
            print(f"Error al obtener categorías: {e}")
            return []
        finally:
            if conn:
                conn.close()