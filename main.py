
import argparse
import csv

from models.tarea import Tarea, SessionLocal
from datetime import datetime, timedelta


def agregar_tarea(descripcion):
    session = SessionLocal()
    nueva_tarea = Tarea(descripcion=descripcion)
    session.add(nueva_tarea)
    session.commit()
    session.refresh(nueva_tarea)
    session.close()
    return nueva_tarea

if __name__ == "__main__":
    tarea = agregar_tarea("Mi primera tarea")
    print(tarea)

def listar_tareas():
    session = SessionLocal()
    tareas = session.query(Tarea).all()
    session.close()
    return tareas

def completar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        tarea.completada = True
        session.commit()
        session.refresh(tarea)
    session.close()
    return tarea

if __name__ == "__main__":
    # Agregar una tarea
    tarea = agregar_tarea("Mi primera tarea")
    print(tarea)

    # Listar todas las tareas
    tareas = listar_tareas()
    print("Todas las tareas:", tareas)

    # Marcar una tarea como completada
    tarea_completada = completar_tarea(tarea.id)
    print("Tarea completada:", tarea_completada)

#Eliminar Tareas.

def eliminar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        session.delete(tarea)
        session.commit()
        resultado = True
    else:
        resultado = False
    session.close()
    return resultado

def buscar_tareas(termino):
    session = SessionLocal()
    tareas = session.query(Tarea).filter(Tarea.descripcion.contains(termino)).all()
    session.close()
    return tareas

if __name__ == "__main__":
    # Agregar una tarea
    tarea = agregar_tarea("Mi primera tarea")
    print(tarea)

    # Listar todas las tareas
    tareas = listar_tareas()
    print("Todas las tareas:", tareas)

    # Marcar una tarea como completada
    tarea_completada = completar_tarea(tarea.id)
    print("Tarea completada:", tarea_completada)

    # Buscar tareas
    tareas_encontradas = buscar_tareas("primera")
    print("Tareas encontradas:", tareas_encontradas)

    # Eliminar una tarea
    eliminada = eliminar_tarea(tarea.id)
    print("Tarea eliminada:", eliminada)

    # Listar todas las tareas después de eliminar
    tareas = listar_tareas()
    print("Todas las tareas después de eliminar:", tareas)


def main():
    parser = argparse.ArgumentParser(description="Gestor de Tareas")
    parser.add_argument('--agregar', type=str, help="Agregar una nueva tarea")
    parser.add_argument('--completar', type=int, help="Marcar una tarea como completada")
    parser.add_argument('--eliminar', type=int, help="Eliminar una tarea")
    parser.add_argument('--buscar', type=str, help="Buscar tareas por descripción")
    parser.add_argument('--listar', action='store_true', help="Listar todas las tareas")

    args = parser.parse_args()

    if args.agregar:
        tarea = agregar_tarea(args.agregar)
        print(f"Tarea agregada: {tarea}")
    elif args.completar:
        tarea = completar_tarea(args.completar)
        if tarea:
            print(f"Tarea completada: {tarea}")
        else:
            print("Tarea no encontrada")
    elif args.eliminar:
        if eliminar_tarea(args.eliminar):
            print("Tarea eliminada")
        else:
            print("Tarea no encontrada")
    elif args.buscar:
        tareas = buscar_tareas(args.buscar)
        print("Tareas encontradas:", tareas)
    elif args.listar:
        tareas = listar_tareas()
        print("Todas las tareas:", tareas)

if __name__ == "__main__":
    main()

from functools import wraps

def manejar_sesion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            resultado = func(session, *args, **kwargs)
            session.commit()
            return resultado
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
    return wrapper

@manejar_sesion
def agregar_tarea(session, descripcion):
    nueva_tarea = Tarea(descripcion=descripcion)
    session.add(nueva_tarea)
    session.refresh(nueva_tarea)
    return nueva_tarea

@manejar_sesion
def completar_tarea(session, tarea_id):
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        tarea.completada = True
        session.refresh(tarea)
    return tarea

@manejar_sesion
def eliminar_tarea(session, tarea_id):
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        session.delete(tarea)
        return True
    return False

@manejar_sesion
def listar_tareas(session):
    return session.query(Tarea).all()

@manejar_sesion
def buscar_tareas(session, termino):
    return session.query(Tarea).filter(Tarea.descripcion.contains(termino)).all()

if __name__ == "__main__":
    main()


#PRIORIDAD DE TAREAS.

tareas = []

def agregar_tarea(nombre, prioridad):
    tareas.append({"nombre": nombre, "prioridad": prioridad})

def asignar_prioridad(tarea_nombre, nueva_prioridad):
    for tarea in tareas:
        if tarea['nombre'] == tarea_nombre:
            tarea['prioridad'] = nueva_prioridad
            return
    print('Tarea no encontrada.')

# agregar algunas tareas
agregar_tarea('Tarea1', 'alta')
agregar_tarea('Tarea2', 'media')

# cambiar la prioridad de una tarea
asignar_prioridad('Tarea2', 'alta')

# imprimir tareas
print(tareas)


def agregar_tarea(nombre, prioridad):
    tareas.append({"nombre": nombre, "prioridad": prioridad})

def obtener_tareas(prioridad):
    return [tarea for tarea in tareas if tarea['prioridad'] == prioridad]

parser = argparse.ArgumentParser(description='Gestión de tareas.')
subparsers = parser.add_subparsers()

parser_agregar = subparsers.add_parser('agregar')
parser_agregar.add_argument('nombre')
parser_agregar.add_argument('prioridad')
parser_agregar.set_defaults(func=lambda args: agregar_tarea(args.nombre, args.prioridad))

parser_listar = subparsers.add_parser('listar')
parser_listar.add_argument('prioridad')
parser_listar.set_defaults(func=lambda args: print(obtener_tareas(args.prioridad)))

args = parser.parse_args()
args.func(args)

#VENCIMIENTO.

def agregar_tarea(nombre, prioridad, fecha_vencimiento):
    # Convertir la fecha de vencimiento de formato string a formato fecha
    fecha_vencimiento = datetime.datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
    tareas.append({"nombre": nombre, "prioridad": prioridad, "fecha_vencimiento": fecha_vencimiento})

# agregar algunas tareas
agregar_tarea('Tarea1', 'alta', '2023-01-01')
agregar_tarea('Tarea2', 'media', '2023-06-10')

# imprimir tareas
for tarea in tareas:
    print(f'Nombre de tarea: {tarea["nombre"]}, Prioridad: {tarea["prioridad"]}, Fecha de vencimiento: {tarea["fecha_vencimiento"].date()}')

def agregar_tarea(nombre, prioridad, vencimiento):
    vencimiento = datetime.strptime(vencimiento, '%Y-%m-%d')
    tareas.append({"nombre": nombre, "prioridad": prioridad, "vencimiento": vencimiento})

def tareas_proximas_a_vencer(dias):
    limite = datetime.now() + timedelta(days=dias)
    return [tarea for tarea in tareas if tarea['vencimiento'] <= limite]

parser = argparse.ArgumentParser(description='Gestor de tareas.')
subparsers = parser.add_subparsers()

parser_agregar = subparsers.add_parser('agregar')
parser_agregar.add_argument('nombre')
parser_agregar.add_argument('prioridad')
parser_agregar.add_argument('vencimiento')
parser_agregar.set_defaults(func=lambda args: agregar_tarea(args.nombre, args.prioridad, args.vencimiento))

parser_proximas_a_vencer = subparsers.add_parser('proximas_a_vencer')
parser_proximas_a_vencer.add_argument('dias', type=int)
parser_proximas_a_vencer.set_defaults(func=lambda args: print(tareas_proximas_a_vencer(args.dias)))

args = parser.parse_args()
args.func(args)

def agregar_tarea(nombre, prioridad, vencimiento):
    vencimiento = datetime.strptime(vencimiento, '%Y-%m-%d')
    tareas.append({"nombre": nombre, "prioridad": prioridad, "vencimiento": vencimiento})

def tareas_proximas_a_vencer(dias):
    limite = datetime.now() + timedelta(days=dias)
    return [tarea for tarea in tareas if tarea['vencimiento'] <= limite]

def exportar_a_csv():
    with open('tareas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Prioridad", "Vencimiento"])
        for tarea in tareas:
            writer.writerow([tarea["nombre"], tarea["prioridad"], tarea["vencimiento"]])

parser = argparse.ArgumentParser(description='Gestor de tareas.')
subparsers = parser.add_subparsers()

parser_agregar = subparsers.add_parser('agregar')
parser_agregar.add_argument('nombre')
parser_agregar.add_argument('prioridad')
parser_agregar.add_argument('vencimiento')
parser_agregar.set_defaults(func=lambda args: agregar_tarea(args.nombre, args.prioridad, args.vencimiento))

parser_proximas_a_vencer = subparsers.add_parser('proximas_a_vencer')
parser_proximas_a_vencer.add_argument('dias', type=int)
parser_proximas_a_vencer.set_defaults(func=lambda args: print(tareas_proximas_a_vencer(args.dias)))

parser_exportar = subparsers.add_parser('exportar')
parser_exportar.set_defaults(func=lambda args: exportar_a_csv())

args = parser.parse_args()
args.func(args)

#Fechas de Vencimiento.

def agregar_tarea(nombre, prioridad, vencimiento):
    vencimiento = datetime.strptime(vencimiento, '%Y-%m-%d')
    tareas.append({"nombre": nombre, "prioridad": prioridad, "vencimiento": vencimiento})

def exportar_tareas():
    with open('tareas.csv', 'w', newline='') as csvfile:
        fieldnames = ['nombre', 'prioridad', 'vencimiento']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for tarea in tareas:
            writer.writerow(tarea)

parser = argparse.ArgumentParser()

parser_add = argparse.ArgumentParser(add_help=False)
parser_add.add_argument('nombre')
parser_add.add_argument('prioridad')
parser_add.add_argument('vencimiento')

subparsers = parser.add_subparsers()
parser_agregar = subparsers.add_parser('agregar', parents=[parser_add])
parser_agregar.set_defaults(func=lambda args: agregar_tarea(args.nombre, args.prioridad, args.vencimiento))

parser_exportar = subparsers.add_parser('exportar')
parser_exportar.set_defaults(func=lambda _: exportar_tareas())

args = parser.parse_args()
args.func(args)


#Exportar Tareas.

def agregar_tarea(nombre, prioridad, vencimiento):
    vencimiento = datetime.strptime(vencimiento, '%Y-%m-%d')
    tareas.append({"nombre": nombre, "prioridad": prioridad, "vencimiento": vencimiento})

def exportar_tareas():
    with open('tareas.csv', 'w', newline='') as csvfile:
        fieldnames = ['nombre', 'prioridad', 'vencimiento']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for tarea in tareas:
            writer.writerow(tarea)

parser = argparse.ArgumentParser()

parser_add = argparse.ArgumentParser(add_help=False)
parser_add.add_argument('nombre')
parser_add.add_argument('prioridad')
parser_add.add_argument('vencimiento')

subparsers = parser.add_subparsers()
parser_agregar = subparsers.add_parser('agregar', parents=[parser_add])
parser_agregar.set_defaults(func=lambda args: agregar_tarea(args.nombre, args.prioridad, args.vencimiento))

parser_exportar = subparsers.add_parser('exportar')
parser_exportar.set_defaults(func=lambda _: exportar_tareas())

args = parser.parse_args()
args.func(args)

#Historial de Tareas Completadas.

def agregar_tarea(nombre, prioridad, vencimiento):
    vencimiento = datetime.strptime(vencimiento, '%Y-%m-%d')
    tareas.append({"nombre": nombre, "prioridad": prioridad, "vencimiento": vencimiento, "completada": False})

def completar_tarea(nombre):
    for tarea in tareas:
        if tarea['nombre'] == nombre:
            tarea['completada'] = True
            return
    print("Tarea no encontrada")

def ver_tareas_completadas():
    return [tarea for tarea in tareas if tarea['completada']]

parser = argparse.ArgumentParser(description='Gestor de tareas.')
subparsers = parser.add_subparsers()

parser_agregar = subparsers.add_parser('agregar')
parser_agregar.add_argument('nombre')
parser_agregar.add_argument('prioridad')
parser_agregar.add_argument('vencimiento')
parser_agregar.set_defaults(func=lambda args: agregar_tarea(args.nombre, args.prioridad, args.vencimiento))

parser_completar = subparsers.add_parser('completar', help='completa una tarea')
parser_completar.add_argument('nombre', help='el nombre de la tarea a completar')
parser_completar.set_defaults(func=lambda args: completar_tarea(args.nombre))

parser_ver_completadas = subparsers.add_parser('ver_completadas', help='ver tareas completadas')
parser_ver_completadas.set_defaults(func=lambda args: print(ver_tareas_completadas()))

args = parser.parse_args()
args.func(args)



# python main.py agregar Tarea1 alta
# python main.py agregar Tarea2 media
# python main.py listar alta
# python main.py agregar Tarea1 alta 2022-12-31
# python main.py agregar Tarea2 media 2022-12-15
# python main.py listar_proximas 30
# python main.py agregar Tarea1 alta 2023-01-31
# python main.py agregar Tarea2 media 2022-12-15
# python main.py proximas_a_vencer 30
# python main.py exportar
# python main.py exportar
# python main.py agregar 'tarea1' 'alta' '2022-12-15'
# python main.py agregar 'tarea2' 'media' '2022-06-10'
# python main.py exportar








   



    