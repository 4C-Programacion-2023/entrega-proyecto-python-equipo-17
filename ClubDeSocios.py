import json
import random
import tkinter as tk
from tkinter import simpledialog, messagebox
import re
from PIL import Image, ImageTk


fechas_simuladas = 0
contador_toques = 0


# Crear la ventana principal
root = tk.Tk()
root.title("Club de Socios")
root.geometry("800x600")
class ObjetoTienda:
    def __init__(self, nombre, descripcion, precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = 0
        self.talla = ""
        self.metodo_pago = ""

def es_correo_gmail(correo):
    # Expresión regular para validar direcciones de correo de Gmail
    patron_gmail = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(patron_gmail, correo)

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
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.partidos_jugados = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
class Partido:
    def __init__(self, equipo_local, equipo_visitante):
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
    ventana_tabla.geometry("800x400")
    ventana_tabla.minsize(600, 200)

    label_titulo = tk.Label(ventana_tabla, text="Tabla de Posiciones", font=("Arial", 16, "bold"))
    label_titulo.pack(pady=10)

    canvas = tk.Canvas(ventana_tabla)
    frame = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(ventana_tabla, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    tabla = tk.Label(frame, text="Posición |    Equipo    | Puntos | PJ | GF | GC", font=("Arial", 12, "bold"))
    tabla.pack()

    equipos_ordenados = sorted(equipos,
                               key=lambda equipo: (equipo.puntos, equipo.goles_a_favor - equipo.goles_en_contra),
                               reverse=True)

    for idx, equipo in enumerate(equipos_ordenados, start=1):
        fila = f"{idx:<9} | {equipo.nombre:<12} | {equipo.puntos:<6} | {equipo.partidos_jugados:<2} | {equipo.goles_a_favor:<2} | {equipo.goles_en_contra:<2}"
        label_equipo = tk.Label(frame, text=fila, font=("Courier New", 10))
        label_equipo.pack()

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    boton_cerrar = tk.Button(ventana_tabla, text="Cerrar", command=ventana_tabla.destroy)
    boton_cerrar.pack(pady=10)


equipos = [Equipo("Talleres"), Equipo("River"), Equipo("Defensa"), Equipo("Boca"),Equipo("Velez"), Equipo("Estudiantes"), Equipo("Colon"), Equipo("Huracan"),Equipo("Independient"), Equipo("  Lanus"), Equipo("Gimnacia"), Equipo("Union"),Equipo("Aldosivi"), Equipo("Argentinos J"), Equipo("Racing"), Equipo("Rosario C"),Equipo("Godoy Cruz"), Equipo("Platense"), Equipo("Newells"), Equipo("Banfiel"),Equipo("San Lorenzo"), Equipo("Central C"), Equipo("Patronato"), Equipo("Sarmiento"),Equipo("Atletico T"), Equipo("Arsenal"), Equipo("Tigre"), Equipo("Barracas C")]



# ... Tu código anterior ...


# Función para simular una fecha de partidos
def simular_fecha():
    global fechas_simuladas, simulacion_en_curso, contador_toques
    if fechas_simuladas < 27:
        simulacion_en_curso = True
    partidos = []
    equipos_disponibles = list(equipos)  # Hacer una copia de la lista de equipos

    while len(equipos_disponibles) >= 2 and len(partidos) < 14:
        equipo_local = random.choice(equipos_disponibles)
        equipos_disponibles.remove(equipo_local)
        equipo_visitante = random.choice(equipos_disponibles)
        equipos_disponibles.remove(equipo_visitante)
        partidos.append(Partido(equipo_local, equipo_visitante))

    for partido in partidos:
        partido.jugar()

        partido.equipo_local.partidos_jugados += 1
        partido.equipo_visitante.partidos_jugados += 1

        partido.equipo_local.goles_a_favor += partido.goles_local
        partido.equipo_local.goles_en_contra += partido.goles_visitante
        partido.equipo_visitante.goles_a_favor += partido.goles_visitante
        partido.equipo_visitante.goles_en_contra += partido.goles_local

        if partido.goles_local > partido.goles_visitante:
            partido.equipo_local.puntos += 3
        elif partido.goles_local < partido.goles_visitante:
            partido.equipo_visitante.puntos += 3
        else:
            partido.equipo_local.puntos += 1
            partido.equipo_visitante.puntos += 1

    contador_toques += 1

    if contador_toques == 27:
        messagebox.showinfo("Fin de la Simulación", "El torneo ha terminado.")
        reiniciar_simulacion()
        # Iniciar el temporizador para reiniciar la simulación después de 2 minutos
        root.after(120000, reiniciar_simulacion)
    else:
        pass



 # Mostrar los resultados de la fecha en una ventana de mensaje
    resultados_fecha = "\n".join([f"{partido.equipo_local.nombre} {partido.goles_local} - {partido.goles_visitante} {partido.equipo_visitante.nombre}" for partido in partidos])
    messagebox.showinfo("Resultados de la Fecha", resultados_fecha)

    # Actualizar la tabla de posiciones en la lista de equipos
    equipos.sort(key=lambda equipo: (equipo.puntos, equipo.goles_a_favor - equipo.goles_en_contra), reverse=True)

# ... Tu código anterior ...
def boton_simular_fecha_click():
    global simulacion_en_curso
    if not simulacion_en_curso:
        simular_fecha()
    else:
        messagebox.showinfo("Simulación en Curso", "La simulación ya está en curso. Espera a que termine.")

carrito = []
objetos_tienda = [
    ObjetoTienda("Remera Titular", "Hecha de tela viscosa, Talles M,L,XL,XXL", 25000),
    ObjetoTienda("Remera Suplente", "Hecha de tela viscosa, Talles S,M,L,XL", 25000),
    ObjetoTienda("Campera T", "Hecha de algodon, Talles S,M,L ", 21660),
    ObjetoTienda("Remera de entrenamiento", "Hecha de tela suave y con friza ,Talles S,M,XL", 11800),
    ObjetoTienda("Gorra T", "Azul y Blanca", 7500),
    ObjetoTienda("Termo de Talleres", "El agua dura caliente 15h", 15000),
    ObjetoTienda("Botella T", "De 2L y de 3L", 3500),
    ObjetoTienda("Medias T", "Medias Blancas y Medias Azules", 4200),
    ObjetoTienda("Short", "Hecho de tela de color Blanco o Azul, Talles S,M,L,XL,XXL", 11400),
    ObjetoTienda("Cervecero", "De 2,5L para tomar Ferned", 8000)
    # Agrega más objetos aquí...
]

def reiniciar_equipos():
    for equipo in equipos:
        equipo.puntos = 0
        equipo.partidos_jugados = 0
        equipo.goles_a_favor = 0
        equipo.goles_en_contra = 0
def reiniciar_simulacion():
    global contador_toques, fechas_simuladas
    contador_toques = 0
    fechas_simuladas = 0
    root.after(120000, reiniciar_equipos)  # Restablecer los datos de los equipos
    messagebox.showinfo("Reinicio de la Simulación", "La simulación y la tabla de posiciones han sido reiniciadas. Puedes comenzar a simular nuevamente.")


def tienda_de_objetos(usuario):
    def volver_a_sesion():
        ventana_tienda.destroy()


    ventana_tienda = tk.Toplevel(root)
    ventana_tienda.title("Tienda de Objetos")
    ventana_tienda.geometry("800x600")

    ventana_tienda.minsize(600, 500)

    canvas = tk.Canvas(ventana_tienda)
    frame = tk.Frame(canvas)

    scrollbar = tk.Scrollbar(ventana_tienda, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))


    boton_volver = tk.Button(ventana_tienda, text="Volver a la sesión", command=volver_a_sesion)
    boton_volver.pack(pady=10)

    def agregar_al_carrito(usuario, objeto):
        talla = simpledialog.askstring("Elegir Talla", f"Elegir talla para {objeto.nombre} (S, M, L, XL, XXL):",
                                       parent=ventana_tienda)

        # Verificar si la talla ingresada es válida
        tallas_validas = ["S", "M", "L", "XL", "XXL"]
        if talla and talla.upper() in tallas_validas:
            objeto.talla = talla.upper()

            metodo_pago = simpledialog.askstring("Elegir Método de Pago", "Elegir método de pago (Débito/Crédito):",
                                                 parent=ventana_tienda)
            if metodo_pago:
                metodo_pago = metodo_pago.lower()  # Convertir a minúsculas para evitar problemas de capitalización
                if metodo_pago in ["debito", "credito"]:
                    objeto.metodo_pago = metodo_pago.capitalize()  # Capitalizar la primera letra
                    carrito.append(objeto)
                    messagebox.showinfo("Agregado al Carrito",
                                        f"Has agregado {objeto.nombre} al carrito con talla '{talla}' y método de pago '{metodo_pago}'.")
                else:
                    messagebox.showerror("Error", "Método de pago no válido. Solo se permiten 'Débito' o 'Crédito'.")
            else:
                messagebox.showerror("Error", "Debes elegir un método de pago.")
        else:
            messagebox.showerror("Error", "Talla no válida. Debes elegir una talla entre S, M, L, XL o XXL.")

        boton_comprar = tk.Button(frame, text="Agregar al Carrito",
                                  command=lambda obj=objeto: agregar_al_carrito(usuario, obj))
        boton_comprar.pack(pady=10, anchor="w")

    def comprar_carrito():
        total = sum(objeto.precio for objeto in carrito)
        if total > 0:
            mensaje = "Objetos en el carrito:\n"
            for objeto in carrito:
                mensaje += f"{objeto.nombre} - ${objeto.precio} - Talla: {objeto.talla} - Método de Pago: {objeto.metodo_pago}\n"
            mensaje += f"\nTotal a Pagar: ${total}"
            respuesta = messagebox.askyesno("Confirmar Compra", f"¿Deseas comprar los siguientes objetos?\n\n{mensaje}")
            if respuesta:
                # Lógica para realizar la compra del carrito por el usuario
                # Aquí puedes actualizar los créditos del usuario, guardar los objetos comprados, etc.
                carrito.clear()  # Limpiar el carrito después de la compra
                messagebox.showinfo("Compra Exitosa", "Has realizado la compra exitosamente.")

    boton_comprar_carrito = tk.Button(frame, text="Comprar Carrito", command=comprar_carrito)
    boton_comprar_carrito.pack(pady=10, anchor="w")



    # Contenido de la tienda de objetos...
    for objeto in objetos_tienda:
        label_nombre = tk.Label(frame, text=objeto.nombre, font=("Arial", 14, "bold"))
        label_nombre.pack(pady=5, anchor="w")

        label_descripcion = tk.Label(frame, text=objeto.descripcion, font=("Arial", 12))
        label_descripcion.pack(pady=2, anchor="w")

        label_precio = tk.Label(frame, text=f"Precio: $ {objeto.precio} Pesos", font=("Arial", 12))
        label_precio.pack(pady=5, anchor="w")

        boton_comprar = tk.Button(frame, text="Agregar al Carrito", command=lambda obj=objeto: agregar_al_carrito(usuario, obj))
        boton_comprar.pack(pady=10, anchor="w")

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


    def comprar_objeto(usuario, objeto):
     carrito.append(objeto)
     messagebox.showinfo("Agregado al Carrito", f"Has agregado {objeto.nombre} al carrito.")

def eliminar_del_carrito(objeto):
    carrito.remove(objeto)
    messagebox.showinfo("Objeto Eliminado", f"{objeto.nombre} ha sido eliminado del carrito.")

def mostrar_carrito(usuario):
    ventana_carrito = tk.Toplevel(root)
    ventana_carrito.title("Carrito de Compras")
    ventana_carrito.geometry("600x500")
    ventana_carrito.minsize(400, 300)

    label_titulo = tk.Label(ventana_carrito, text="Carrito de Compras", font=("Arial", 16, "bold"))
    label_titulo.pack(pady=10)

    canvas = tk.Canvas(ventana_carrito)
    frame = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(ventana_carrito, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    for objeto in carrito:
        label_objeto = tk.Label(frame, text=f"{objeto.nombre} - ${objeto.precio}", font=("Arial", 12))
        label_objeto.pack(pady=5, anchor="w")

        boton_eliminar = tk.Button(frame, text="Eliminar", command=lambda obj=objeto: eliminar_del_carrito(obj))
        boton_eliminar.pack(pady=5, anchor="w")

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


def mostrar_ventana_sesion(usuario,):
    def cerrar_sesion():
        # Mostrar la ventana principal
        root.deiconify()
        # Destruir la ventana de sesión
        ventana_sesion.destroy()

    ventana_sesion = tk.Toplevel(root)
    ventana_sesion.title(f"Bienvenido, {usuario}!")
    ventana_sesion.geometry("800x700")
    ventana_sesion.minsize(500, 400)
    # Resto del contenido de la nueva ventana...
    # Puedes agregar widgets, botones y otras funcionalidades aquí.
    # Cargar la imagen de fondo



    # Crear el botón para cerrar sesión
    boton_cerrar_sesion = tk.Button(ventana_sesion, text="Cerrar Sesión", command=cerrar_sesion, width=20, height=2, font=("Arial", 14))
    boton_cerrar_sesion.pack(pady=10)

    boton_cerrar_sesion.pack(side=tk.RIGHT, anchor=tk.SE)

    boton_simular_fecha_click = tk.Button(ventana_sesion, text="Simular Fecha", command=simular_fecha, width=40, height=3, font=("Arial", 14))
    boton_simular_fecha_click.pack(pady=10)

    boton_mostrar_tabla = tk.Button(ventana_sesion, text="Mostrar Tabla de Posiciones",command=lambda: mostrar_tabla_posiciones(equipos), width=40, height=3, font=("Arial", 14))
    boton_mostrar_tabla.pack(pady=10)

    boton_tienda = tk.Button(ventana_sesion, text="Ir a la Tienda", command=lambda: tienda_de_objetos(usuario), width=40, height=3, font=("Arial", 14))
    boton_tienda.pack(pady=10)

    boton_carrito = tk.Button(ventana_sesion, text="Ir al Carrito", command=lambda: mostrar_carrito(usuario), width=40, height=3, font=("Arial", 14))
    boton_carrito.pack(pady=10)

def validar_fecha(fecha):
    try:
        dia, mes, año = map(int, fecha.split('/'))
        if 1 <= mes <= 12 and 1 <= dia <= 31:
            return True
        else:
            return False
    except ValueError:
        return False

def registrar_socio():
    usuario = simpledialog.askstring("Registro de Socio", "Nuevo Usuario:")
    contrasena = simpledialog.askstring("Registro de Socio", "Nueva Contraseña:", show="*")
    email = simpledialog.askstring("Registro de Socio", "Dirección de correo electrónico:")
    fecha_nacimiento = simpledialog.askstring("Registro de Socio", "Fecha de nacimiento (DD/MM/AAAA):")

    if usuario and contrasena and email and fecha_nacimiento:
        if usuario in socios_registrados:
            messagebox.showerror("Registro de Socio", "El usuario ya está registrado.")
        elif not es_correo_gmail(email):
            messagebox.showerror("Registro de Socio", "Ingresa una dirección de correo Gmail válida.")
        elif not validar_fecha(fecha_nacimiento):
            messagebox.showerror("Registro de Socio", "La fecha de nacimiento no es válida.")
        else:
            socios_registrados[usuario] = {
                "contrasena": contrasena,
                "email": email,
                "fecha_nacimiento": fecha_nacimiento
            }
            credenciales_socios[usuario] = contrasena
            messagebox.showinfo("Registro de Socio", "Registro exitoso. ¡Bienvenido!")
            root.withdraw()
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

# ... Tu código anterior ...

boton_iniciar_sesion = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, width=40, height=3, font=("Arial", 14), highlightthickness=0, highlightbackground=root.cget("bg"))
boton_iniciar_sesion.pack(pady=10, anchor="center")

boton_registrar_socio = tk.Button(root, text="Registrar Socio", command=registrar_socio, width=40, height=3, font=("Arial", 14), highlightthickness=0, highlightbackground=root.cget("bg"))
boton_registrar_socio.pack(pady=10, anchor="center")

boton_reservar_instalaciones = tk.Button(root, text="Reservar Instalaciones", command=reservar_instalaciones, width=40, height=3, font=("Arial", 14), highlightthickness=0, highlightbackground=root.cget("bg"))
boton_reservar_instalaciones.pack(pady=10, anchor="center")

boton_consultar_eventos = tk.Button(root, text="Consultar Eventos", command=consultar_eventos, width=40, height=3, font=("Arial", 14), highlightthickness=0, highlightbackground=root.cget("bg"))
boton_consultar_eventos.pack(pady=10, anchor="center")

# ... Tu código posterior ...


def salir():
    # Guardar los socios registrados y las credenciales de inicio de sesión al cerrar el programa
    guardar_socios_registrados(socios_registrados)
    guardar_credenciales_socios(credenciales_socios)
    root.destroy()  # Cierra la ventana principal

# Crear el botón para salir
boton_salir = tk.Button(root, text="Salir", command=salir, width=40, height=3, font=("Arial", 14))
boton_salir.pack(pady=10, anchor="center")

root.mainloop()