import psycopg2

def conexion():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="SaborLocal",
            user="postgres",
            password="123456"
        )
        return conn  
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
