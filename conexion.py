import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",           
            password="root",  
            database="Solicitud_Vacaciones"
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos Solicitud_Vacaciones...")
            return conexion
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)
        return None

if __name__ == "__main__":
    conectar()
