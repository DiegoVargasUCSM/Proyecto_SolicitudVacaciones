from conexion import conectar
from datetime import datetime


def validar_int(mensaje):
    while True:
        valor = input(mensaje)
        if valor.isdigit():
            return int(valor)
        print("Solo se permiten números...")

def validar_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor != "":
            return valor
        print("Este campo no puede estar vacío...")

def validar_fecha(mensaje):
    while True:
        fecha = input(mensaje)
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("Formato inválido. Use YYYY-MM-DD.")



def insertar_empleado():
    conexion = conectar()
    if not conexion:
        return
    cursor = conexion.cursor()

    print("\n--- Insertar Empleado ---")
    DNI = validar_int("DNI: ")
    nombre = validar_texto("Apellidos y nombres: ")
    fecha = validar_fecha("Fecha de ingreso (YYYY-MM-DD): ")
    dependencia = validar_texto("Dependencia: ")
    cargo = validar_texto("Cargo: ")
    idArea = validar_int("ID de Área: ")
    idSolicitud = validar_int("ID de Solicitud: ")
    tipo = validar_texto("Tipo de régimen (DL 1057 o DL 276): ")

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

    DNI = validar_int("Ingrese el DNI del empleado: ")

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
    nueva_dependencia = validar_texto("Nueva dependencia: ")
    nuevo_cargo = validar_texto("Nuevo cargo: ")
    nuevo_id_area = validar_int("Nuevo idArea: ")

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
    DNI = validar_int("DNI del empleado: ")

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
        print("1. Colaboradores por régimen laboral")
        print("2. Vacaciones por mes")
        print("3. Empleados y cargos")
        print("4. Colaboradores con vacaciones solicitadas")
        print("5. Cruces de periodos vacacionales")
        print("6. Días disponibles de vacaciones")
        print("7. Cargos y fechas de vacaciones")
        print("8. Total de colaboradores por área")
        print("9. Solicitudes ordenadas por fecha")
        print("10. Observaciones registradas")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        reportes = {
            "1": 'reporte_colaboradores_por_regimen',
            "2": 'reporte_vacaciones_por_mes',
            "3": 'reporte_empleados_cargo',
            "4": 'reporte_colaboradores_con_vacaciones',
            "5": 'reporte_cruce_vacaciones',
            "6": 'reporte_dias_disponibles',
            "7": 'reporte_cargos_vacaciones',
            "8": 'reporte_colaboradores_por_area',
            "9": 'reporte_solicitudes_ordenadas',
            "10": 'reporte_observaciones'
        }

        if opcion in reportes:
            mostrar_reporte(reportes[opcion])
        elif opcion == "0":
            break
        else:
            print("Opción no válida...")


def menu_desarrollador():
    while True:
        print("\n--- MENÚ DE DESARROLLADOR ---")
        print("1. Insertar empleado")
        print("2. Actualizar empleado")
        print("3. Eliminar empleado")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_empleado()
        elif opcion == "2":
            actualizar_empleado()
        elif opcion == "3":
            eliminar_empleado()
        elif opcion == "0":
            break
        else:
            print("Opción inválida...")


if __name__ == "__main__":
    while True:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Módulo Desarrollador")
        print("2. Módulo Reportes")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_desarrollador()
        elif opcion == "2":
            menu_reportes()
        elif opcion == "3":
            print("\nSaliendo del sistema...")
            break
        else:
            print("Opción no válida...")
