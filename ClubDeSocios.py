import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import random

root = tk.Tk()
root.title("Club de Socios")
root.geometry("800x600")

class ObjetoTienda:
    def _init_(self, nombre, descripcion, precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

# Función para cargar los socios registrados desde un archivo JSON
def cargar_socios_registrados():
    try:
        with open("socios_registrados.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Función para cargar las credenciales de inicio de sesión desde un archivo JSON
def cargar_credenciales_socios():
    try:
        with open("credenciales_socios.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Función para guardar los socios registrados en un archivo JSON
def guardar_socios_registrados(socios_registrados):
    with open("socios_registrados.json", "w") as file:
        json.dump(socios_registrados, file)

# Función para guardar las credenciales de inicio de sesión en un archivo JSON
def guardar_credenciales_socios(credenciales_socios):
    with open("credenciales_socios.json", "w") as file:
        json.dump(credenciales_socios, file)

# Cargar los socios registrados y las credenciales de inicio de sesión al iniciar el programa
socios_registrados = cargar_socios_registrados()
credenciales_socios = cargar_credenciales_socios()

def iniciar_sesion():
    usuario = simpledialog.askstring("Iniciar Sesión", "Usuario:")
    contrasena = simpledialog.askstring("Iniciar Sesión", "Contraseña:", show="*")

    if usuario in credenciales_socios and credenciales_socios[usuario] == contrasena:
        messagebox.showinfo("Inicio de Sesión", f"Bienvenido, {usuario}!")
        # Ocultar la ventana principal
        root.withdraw()
        # Mostrar la nueva ventana
        mostrar_ventana_sesion(usuario)
    else:
        messagebox.showerror("Inicio de Sesión", "Usuario o contraseña incorrectos.")

class Equipo:
    def _init_(self, nombre):
        self.nombre = nombre
        self.puntos = 0
class Partido:
    def _init_(self, equipo_local, equipo_visitante):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.goles_local = 0
        self.goles_visitante = 0

    def jugar(self):
        self.goles_local = random.randint(0, 5)
        self.goles_visitante = random.randint(0, 5)

def mostrar_tabla_posiciones(equipos):
    ventana_tabla = tk.Toplevel(root)
    ventana_tabla.title("Tabla de Posiciones")
    ventana_tabla.geometry("400x400")

    label_titulo = tk.Label(ventana_tabla, text="Tabla de Posiciones", font=("Arial", 16, "bold"))
    label_titulo.pack(pady=10)

    tabla = tk.Label(ventana_tabla, text="Posición | Equipo | Puntos", font=("Arial", 14, "bold"))
    tabla.pack()

    equipos_ordenados = sorted(equipos, key=lambda equipo: equipo.puntos, reverse=True)

    for idx, equipo in enumerate(equipos_ordenados, start=1):
        fila = f"{idx:8} | {equipo.nombre:20} | {equipo.puntos}"
        label_equipo = tk.Label(ventana_tabla, text=fila)
        label_equipo.pack()

    boton_cerrar = tk.Button(ventana_tabla, text="Cerrar", command=ventana_tabla.destroy)
    boton_cerrar.pack(pady=10)

equipos = [Equipo("Talleres"), Equipo("River"), Equipo("Defensa"), Equipo("Boca"),Equipo("Velez"), Equipo("Estudiantes"), Equipo("Colon"), Equipo("Huracan"),Equipo("Independiente"), Equipo("  Lanus"), Equipo("Gimnacia"), Equipo("Union"),Equipo("Aldosivi"), Equipo("Argentinos Juniors"), Equipo("Racing"), Equipo("Rosario Central"),Equipo("Godoy Cruz"), Equipo("Platense"), Equipo("Newells"), Equipo("Banfiel"),Equipo("San Lorenzo"), Equipo("Central Cordoba"), Equipo("Patronato"), Equipo("Sarmiento"),Equipo("Atletico Tucuman"), Equipo("Arsenal"), Equipo("Tigre"), Equipo("Barracas central")]



# ... Tu código anterior ...


# Función para simular una fecha de partidos
def simular_fecha():
    partidos = []
    for i in range(len(equipos)):
        for j in range(i + 1, len(equipos)):
            partidos.append(Partido(equipos[i], equipos[j]))

    for partido in partidos:
        partido.jugar()

        if partido.goles_local > partido.goles_visitante:
            partido.equipo_local.puntos += 3
            partido.equipo_local.diferencia_goles += partido.goles_local - partido.goles_visitante
        elif partido.goles_local < partido.goles_visitante:
            partido.equipo_visitante.puntos += 3
            partido.equipo_visitante.diferencia_goles += partido.goles_visitante - partido.goles_local
        else:
            partido.equipo_local.puntos += 1
            partido.equipo_visitante.puntos += 1

    # Mostrar los resultados de la fecha en una ventana de mensaje
    resultados_fecha = "\n".join([f"{partido.equipo_local.nombre} {partido.goles_local} - {partido.goles_visitante} {partido.equipo_visitante.nombre}" for partido in partidos])
    messagebox.showinfo("Resultados de la Fecha", resultados_fecha)

    # Actualizar la tabla de posiciones en la lista de equipos
    equipos.sort(key=lambda equipo: (equipo.puntos, equipo.diferencia_goles), reverse=True)

# ... Tu código anterior ...


def tienda_de_objetos(usuario):
    def volver_a_sesion():
        ventana_tienda.destroy()
        mostrar_ventana_sesion(usuario)

    ventana_tienda = tk.Toplevel(root)
    ventana_tienda.title("Tienda de Objetos")
    ventana_tienda.geometry("800x600")

    canvas = tk.Canvas(ventana_tienda)
    frame = tk.Frame(canvas)

    scrollbar = tk.Scrollbar(ventana_tienda, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    # Lista de objetos disponibles en la tienda
    objetos_tienda = [
        ObjetoTienda("Remera Titular", "Hecha de tela viscosa, Talles M,L,XL,XXL", 25000),
        ObjetoTienda("Remera Suplente", "Descripción del Objeto 2", 25000),
        ObjetoTienda("Campera T", "Hecha de algodon, Talles S,M,L ", 21660),
        ObjetoTienda("Remera de entrenamiento", "Hecha de tela y con una friza ,Talles S,M,XL", 11800),
        ObjetoTienda("Gorra T", "Azul y Blanca", 7500),
        ObjetoTienda("Termo de Talleres", "El agua dura caliente 15h", 15000),
        ObjetoTienda("Botella T", "De 2L y de 3L", 3500),
        ObjetoTienda("Medias T", "Medias Blancas y Medias Azules", 4200),
        ObjetoTienda("Short", "Hecho de tela de color Blanco o Azul, Talles S,M,L,XL,XXL", 11400),
        ObjetoTienda("Cervecero", "De 2,5L para tomar Ferned", 8000)
        # Agrega más objetos aquí...
    ]

    boton_volver = tk.Button(ventana_tienda, text="Volver a la sesión", command=volver_a_sesion)
    boton_volver.pack(pady=10)

    # Contenido de la tienda de objetos...
    for objeto in objetos_tienda:
        label_nombre = tk.Label(frame, text=objeto.nombre, font=("Arial", 14, "bold"))
        label_nombre.pack(pady=5, anchor="w")

        label_descripcion = tk.Label(frame, text=objeto.descripcion, font=("Arial", 12))
        label_descripcion.pack(pady=2, anchor="w")

        label_precio = tk.Label(frame, text=f"Precio: $ {objeto.precio} Pesos", font=("Arial", 12))
        label_precio.pack(pady=5, anchor="w")

        boton_comprar = tk.Button(frame, text="Comprar", command=lambda obj=objeto: comprar_objeto(usuario, obj))
        boton_comprar.pack(pady=10, anchor="w")

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def comprar_objeto(usuario, objeto):
    # Lógica para realizar la compra del objeto por el usuario
    # Aquí puedes actualizar los créditos del usuario, guardar el objeto comprado, etc.
    messagebox.showinfo("Compra Exitosa", f"Has comprado {objeto.nombre} por $ {objeto.precio} Pesos.")


def mostrar_ventana_sesion(usuario,):
    def cerrar_sesion():
        # Mostrar la ventana principal
        root.deiconify()
        # Destruir la ventana de sesión
        ventana_sesion.destroy()

    ventana_sesion = tk.Toplevel(root)
    ventana_sesion.title(f"Bienvenido, {usuario}!")
    ventana_sesion.geometry("800x700")
    # Resto del contenido de la nueva ventana...
    # Puedes agregar widgets, botones y otras funcionalidades aquí.

    # Crear el botón para cerrar sesión
    boton_cerrar_sesion = tk.Button(ventana_sesion, text="Cerrar Sesión", command=cerrar_sesion)
    boton_cerrar_sesion.pack(pady=10)

    boton_cerrar_sesion.pack(side=tk.RIGHT, anchor=tk.SE)

    boton_tienda = tk.Button(ventana_sesion, text="Ir a la Tienda", command=lambda: tienda_de_objetos(usuario))
    boton_tienda.pack(pady=10)

    boton_simular_fecha = tk.Button(ventana_sesion, text="Simular Fecha", command=simular_fecha)
    boton_simular_fecha.pack(pady=10)

    boton_mostrar_tabla = tk.Button(ventana_sesion, text="Mostrar Tabla de Posiciones",command=lambda: mostrar_tabla_posiciones(equipos))
    boton_mostrar_tabla.pack(pady=10)


def registrar_socio():
    usuario = simpledialog.askstring("Registro de Socio", "Nuevo Usuario:")
    contrasena = simpledialog.askstring("Registro de Socio", "Nueva Contraseña:", show="*")
    email = simpledialog.askstring("Registro de Socio", "Dirección de correo electrónico:")
    fecha_nacimiento = simpledialog.askstring("Registro de Socio", "Fecha de nacimiento (DD/MM/AAAA):")

    if usuario and contrasena and email and fecha_nacimiento:  # Verifica si se ingresaron datos válidos
        if usuario in socios_registrados:
            messagebox.showerror("Registro de Socio", "El usuario ya está registrado.")
        else:
            socios_registrados[usuario] = {
                "contrasena": contrasena,
                "email": email,
                "fecha_nacimiento": fecha_nacimiento
            }
            credenciales_socios[usuario] = contrasena
            messagebox.showinfo("Registro de Socio", "Registro exitoso. ¡Bienvenido!")
            # Ocultar la ventana principal
            root.withdraw()
            # Mostrar la nueva ventana
            mostrar_ventana_sesion(usuario)


def reservar_instalaciones():
    # Aquí irá la lógica para realizar una reserva de instalaciones
    pass

def consultar_eventos():
    # Aquí irá la lógica para consultar los eventos del club
    pass

# Resto del código...

label_titulo = tk.Label(root, text="¡Bienvenido al Club de Socios!", font=("Arial", 24))
label_titulo.pack(pady=20)

boton_iniciar_sesion = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack(pady=10)

boton_registrar_socio = tk.Button(root, text="Registrar Socio", command=registrar_socio)
boton_registrar_socio.pack(pady=10)

boton_reservar_instalaciones = tk.Button(root, text="Reservar Instalaciones", command=reservar_instalaciones)
boton_reservar_instalaciones.pack(pady=10)

boton_consultar_eventos = tk.Button(root, text="Consultar Eventos", command=consultar_eventos)
boton_consultar_eventos.pack(pady=10)


def salir():
    # Guardar los socios registrados y las credenciales de inicio de sesión al cerrar el programa
    guardar_socios_registrados(socios_registrados)
    guardar_credenciales_socios(credenciales_socios)
    root.destroy()  # Cierra la ventana principal

# Crear el botón para salir
boton_salir = tk.Button(root, text="Salir", command=salir)
boton_salir.pack(pady=10)

root.mainloop()

"comentario"