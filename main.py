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

    print(f"\n--- Resultado del {nombre_reporte} ---\n")

    for resultado in cursor.stored_results():
        filas = resultado.fetchall()
        columnas = [desc[0] for desc in resultado.description]

        anchos = []
        for i in range(len(columnas)):
            max_fila = max((len(str(f[i])) for f in filas), default=0)
            anchos.append(max(len(columnas[i]), max_fila) + 2)

        encabezado = " | ".join(f"{col:<{anchos[i]}}" for i, col in enumerate(columnas))
        print(encabezado)
        print("-" * len(encabezado))

        for fila in filas:
            print(" | ".join(f"{str(fila[i]):<{anchos[i]}}" for i in range(len(fila))))

    cursor.close()
    conexion.close()


def menu_reportes():
    while True:
        print("\n--- MENÚ DE REPORTES ---")
        print("1. Colaboradores por regimen laboral")
        print("2. Vacaciones por mes")
        print("3. Empleados y cargos")
        print("4. Colaboradores con vacaciones solicitadas")
        print("5. Cruces de periodos vacacionales")
        print("6. Dias disponibles de vacaciones")
        print("7. Cargos y fechas de vacaciones")
        print("8. Total de colaboradores por area")
        print("9. Solicitudes ordenadas por fecha")
        print("10. Observaciones registradas")
        print("0. Volver al menu principal....")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            mostrar_reporte('reporte_colaboradores_por_regimen')
        elif opcion == "2":
            mostrar_reporte('reporte_vacaciones_por_mes')
        elif opcion == "3":
            mostrar_reporte('reporte_empleados_cargo')
        elif opcion == "4":
            mostrar_reporte('reporte_colaboradores_con_vacaciones')
        elif opcion == "5":
            mostrar_reporte('reporte_cruce_vacaciones')
        elif opcion == "6":
            mostrar_reporte('reporte_dias_disponibles')
        elif opcion == "7":
            mostrar_reporte('reporte_cargos_vacaciones')
        elif opcion == "8":
            mostrar_reporte('reporte_colaboradores_por_area')
        elif opcion == "9":
            mostrar_reporte('reporte_solicitudes_ordenadas')
        elif opcion == "10":
            mostrar_reporte('reporte_observaciones')
        elif opcion == "0":
            break


def menu_desarrollador():
    while True:
        print("\n--- MENÚ DESARROLLADOR ---")
        print("1. Insertar empleado")
        print("2. Actualizar empleado")
        print("3. Eliminar empleado")
        print("4. Volver al menú principal")

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
            print("Opción inválida.")


def menu_principal():
    while True:
        print("\n=========== MENÚ PRINCIPAL ===========")
        print("1. Desarrollador (CRUD)")
        print("2. Reportes")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_desarrollador()
        elif opcion == "2":
            menu_reportes()
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")



if __name__ == "__main__":
    menu_principal()
