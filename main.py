from conexion import conectar

def insertar_empleado():
    conexion = conectar()
    if not conexion:
        return
    cursor = conexion.cursor()
    print("\n--- Insertar Empleado ---")
    DNI = int(input("DNI: "))
    nombre = input("Apellidos y nombres: ")
    fecha = input("Fecha de ingreso (YYYY-MM-DD): ")
    dependencia = input("Dependencia: ")
    cargo = input("Cargo: ")
    idArea = int(input("ID de Área: "))
    idSolicitud = int(input("ID de Solicitud: "))
    tipo = input("Tipo de régimen (DL 1057 o DL 276): ")

    cursor.callproc('insertar_empleado', [DNI, nombre, fecha, dependencia, cargo, idArea, idSolicitud, tipo])
    conexion.commit()
    print("\nEmpleado insertado correctamente...")
    cursor.close()
    conexion.close()


def actualizar_empleado():
    conexion = conectar()
    if not conexion:
        return

    cursor = conexion.cursor(dictionary=True)
    print("\n--- Actualizar Empleado ---")

    DNI = input("Ingrese el DNI del empleado: ")
    cursor.execute("SELECT * FROM Empleado WHERE DNI = %s", (DNI,))
    empleado = cursor.fetchone()

    if not empleado:
        print("No se encontró un empleado con ese DNI...")
        cursor.close()
        conexion.close()
        return

    print("\nDatos actuales del empleado:")
    for clave, valor in empleado.items():
        print(f"{clave}: {valor}")

    print("\n--- Ingrese los nuevos datos ---")
    nueva_dependencia = input("Nueva dependencia: ")
    nuevo_cargo = input("Nuevo cargo: ")
    nuevo_id_area = int(input("Nuevo idArea: "))

    cursor.callproc('actualizar_empleado', [DNI, nueva_dependencia, nuevo_cargo, nuevo_id_area])
    conexion.commit()
    print("\nDatos actualizados correctamente...")

    cursor.close()
    conexion.close()



def eliminar_empleado():
    conexion = conectar()
    if not conexion:
        return
    cursor = conexion.cursor()
    print("\n--- Eliminar Empleado ---")
    DNI = int(input("DNI del empleado: "))
    cursor.callproc('eliminar_empleado', [DNI])
    conexion.commit()
    print("\nEmpleado eliminado correctamente...")
    cursor.close()
    conexion.close()

def mostrar_reporte(nombre_reporte):
    conexion = conectar()
    if not conexion:
        return
    cursor = conexion.cursor()
    cursor.callproc(nombre_reporte)

    print("\n--- Resultado del {nombre_reporte} ---")
    for resultado in cursor.stored_results():
        filas = resultado.fetchall()
        for fila in filas:
            print(fila)
    cursor.close()
    conexion.close()

if __name__ == "__main__":
    while True:
        print("\n--- MENÚ ---")
        print("1. Insertar empleado")
        print("2. Actualizar empleado")
        print("3. Eliminar empleado")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_empleado()
        elif opcion == "2":
            actualizar_empleado()
        elif opcion == "3":
            eliminar_empleado()
        elif opcion == "4":
            break
        else:
            print("Opción no válida...")

