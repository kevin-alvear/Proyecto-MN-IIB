import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para calcular la dinámica poblacional utilizando la ecuación logística
def logistic_map(rate, initial_pop, steps=100):
    population = np.zeros(steps)
    population[0] = initial_pop
    for i in range(1, steps):
        population[i] = rate * population[i - 1] * (1 - population[i - 1])
    return population


# Función para detectar los puntos de bifurcación
def find_bifurcation_points(r_start=2.5, r_end=4.0, steps=10000, threshold=1e-6):
    r_values = np.linspace(r_start, r_end, steps)
    x = 1e-5 * np.ones(steps)
    bifurcation_points = []

    for i in range(1000):
        x = r_values * x * (1 - x)
        if i >= 900:
            # Calcular diferencias en los puntos
            delta_x = np.abs(np.diff(x))
            # Encontrar puntos donde la diferencia es muy pequeña
            potential_bifurcations = r_values[:-1][delta_x < threshold]
            bifurcation_points.extend(potential_bifurcations)

    # Filtrar valores únicos
    bifurcation_points = np.unique(np.round(bifurcation_points, decimals=3))
    return bifurcation_points


# Llamada a la función para detectar y mostrar los puntos de bifurcación
bifurcation_points = find_bifurcation_points()
print(f"Puntos de bifurcación detectados: {bifurcation_points}")


# Función para actualizar la gráfica de bifurcación
def plot_bifurcation():
    ax.clear()
    ax.set_xlabel('Tasa de Crecimiento (f)', fontsize=12)
    ax.set_ylabel('Población', fontsize=12)
    ax.set_title('Diagrama de Bifurcación', fontsize=14)
    ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)




    r_values = np.linspace(0, 4, 1000)
    initial_pop = initial_pop_slider.get()
    last_values = 100  # Número de valores finales para visualizar la bifurcación

    for r in r_values:
        pop = logistic_map(r, initial_pop, 1000)
        ax.plot([r] * last_values, pop[-last_values:], ',k', alpha=0.25)

    canvas.draw()


# Función para mostrar los valores de los sliders
def update_rate(*args):
    rate_value_label.config(text=f"{rate_slider.get():.2f}")

def update_initial_pop(*args):
    initial_pop_value_label.config(text=f"{initial_pop_slider.get():.2f}")

# Función para iniciar la animación
def start_animation():
    global population, steps
    rate = rate_slider.get()
    initial_pop = initial_pop_slider.get()
    steps = 10

    population = logistic_map(rate, initial_pop, steps)
    animate_plot()

# Función para actualizar la gráfica de forma animada
def animate_plot(i=0):
    if i == 0:
        ax.clear()
        ax.set_ylim(0, 1)
        ax.set_xlim(0, steps - 1)
        ax.set_xlabel('Tiempo', fontsize=12)
        ax.set_ylabel('Población', fontsize=12)
        ax.set_title('Dinámica de la Población', fontsize=14)
        ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)

    if i < steps:
        ax.plot(range(i + 1), population[:i + 1], marker='o', color='#007acc', linestyle='-', linewidth=2)
        canvas.draw()
        root.after(200, animate_plot, i + 1)

# Función para reiniciar los valores de los sliders
def reset_sliders():
    rate_slider.set(2.0)
    initial_pop_slider.set(0.75)

# Función para limpiar la gráfica
def clear_plot():
    ax.clear()
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 20)
    canvas.draw()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Dinámica Poblacional")
root.configure(bg="#f4f4f4")  # Fondo claro

# Establecer tamaño de la ventana
root.geometry("1280x720")

# Crear la figura y el eje para la gráfica
fig, ax = plt.subplots(figsize=(10, 7), dpi=100)  # Aumenta el tamaño de la figura
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=1, rowspan=7, padx=20, pady=20)

# Crear un marco para los controles
control_frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Crear controles de la interfaz gráfica
ttk.Label(control_frame, text="Tasa de Crecimiento (f)", style="TLabel").grid(row=0, column=0, sticky="w")

# Slider Rate
rate_slider = ttk.Scale(control_frame, from_=0.0, to=4.0, orient="horizontal")
rate_slider.set(2.0)
rate_slider.grid(row=1, column=0, sticky="ew", pady=5)

# Definición de la etiqueta para mostrar el valor del slider Rate
rate_value_label = ttk.Label(control_frame, text="2.00", style="TLabel")
rate_value_label.grid(row=1, column=1, sticky="w", padx=5)

# Conectar el slider a la función de actualización
rate_slider.bind("<Motion>", update_rate)

ttk.Label(control_frame, text="Población Inicial (P0)", style="TLabel").grid(row=2, column=0, sticky="w")

# Slider Initial Pop
initial_pop_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, orient="horizontal")
initial_pop_slider.set(0.75)
initial_pop_slider.grid(row=3, column=0, sticky="ew", pady=5)

# Definición de la etiqueta para mostrar el valor del slider Initial Pop
initial_pop_value_label = ttk.Label(control_frame, text="0.75", style="TLabel")
initial_pop_value_label.grid(row=3, column=1, sticky="w", padx=5)

# Conectar el slider a la función de actualización
initial_pop_slider.bind("<Motion>", update_initial_pop)

# Botón para iniciar la animación
play_button = ttk.Button(control_frame, text="Iniciar Animación", command=start_animation, style="TButton")
play_button.grid(row=4, column=0, pady=5, sticky="ew")

# Botón para graficar la bifurcación
bifurcation_button = ttk.Button(control_frame, text="Graficar Bifurcación", command=plot_bifurcation, style="TButton")
bifurcation_button.grid(row=5, column=0, pady=5, sticky="ew")

# Botón para reiniciar los sliders
reset_button = ttk.Button(control_frame, text="Reiniciar", command=reset_sliders, style="TButton")
reset_button.grid(row=6, column=0, pady=5, sticky="ew")

# Botón para limpiar la gráfica
clear_button = ttk.Button(control_frame, text="Limpiar Gráfica", command=clear_plot, style="TButton")
clear_button.grid(row=7, column=0, pady=5, sticky="ew")

# Configurar las columnas para que se ajusten al tamaño del contenido
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_rowconfigure(0, weight=1)

# Aplicar estilos personalizados a los widgets
style = ttk.Style()
style.configure("TFrame", background="#f4f4f4")
style.configure("TLabel", background="#f4f4f4", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10), padding=6)
style.configure("TScale", background="#f4f4f4")

# Ejecutar la aplicación
root.mainloop()
