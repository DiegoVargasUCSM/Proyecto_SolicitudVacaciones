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
    cursor.execute("SELECT * FROM empleados WHERE DNI = %s", (DNI,))
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
    nuevo_id_solicitud = int(input("Nuevo idSolicitud: "))

    cursor.callproc('actualizar_empleado', [DNI, nueva_dependencia, nuevo_cargo, nuevo_id_area, nuevo_id_solicitud])
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
