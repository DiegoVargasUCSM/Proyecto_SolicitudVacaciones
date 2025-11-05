from conexion import conectar

def insertar_empleado():
    conexion = conectar()
    if not conexion:
        return
    cursor = conexion.cursor()
    print("\n---Insertar Empleados---")
    DNI = int(input("DNI: "))
    nombre = input("Apellidos y nombres: ")
    fecha = input("Fecha de ingreso: ")
    dependencia = input("Dependencia: ")
    cargo = input("Cargo: ")
    idArea = int(input("ID de Area: "))
    idSolicitud = int(input("ID de Solicitud: "))
    tipo = input("Tipo de regimen (DL 1057 o DL 276)")

    cursor.callproc('insertar_empleado',[DNI, nombre, fecha, dependencia, cargo, idArea, idSolicitud, tipo])
    conexion.commit()
    print("Empleado insertado correctamente...")
    cursor.close()
    conexion.close()

def actualizar_empleado():
    conexion = conectar()
    if not conexion:
        return
    cursor = conexion.cursor()
    DNI = input("DNI a actualizar: ") or None
    nombre = input("Nuevo Apellidos y Nombres: ") or None
    dependencia = input("Nueva Dependencia: ") or None 
    cargo = input("Nuevo Cargo: ") or None
    idArea = input("Nuevo idArea (o vacío): ") or None
    idSolicitud  = input("Nuevo idSolicitud (o vacío): ") or None
    cursor.callproc('actualizar_empleado', [DNI, nombre, dependencia, cargo, idArea, idSolicitud])
    conexion.commit()
    print("Empleado actualizado correctamente...")
    cursor.close()
    conexion.close()