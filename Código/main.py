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
def find_bifurcation_points(r_start=1, r_end=4.0, steps=10000, threshold=1e-6):
    r_values = np.linspace(r_start, r_end, steps)
    x = 1e-5 * np.ones(steps)
    bifurcation_points = []

    for i in range(1000):
        x = r_values * x * (1 - x)
        if i >= 900:
            delta_x = np.abs(np.diff(x))
            potential_bifurcations = r_values[:-1][delta_x < threshold]
            bifurcation_points.extend(potential_bifurcations)

    bifurcation_points = np.unique(np.round(bifurcation_points, decimals=3))
    return bifurcation_points

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

    # Actualizar los puntos de bifurcación en la interfaz gráfica
    bifurcation_points = find_bifurcation_points()
    bifurcation_label.config(text=f"Puntos de bifurcación: {', '.join(map(str, bifurcation_points))}")

    # Marcar los puntos de bifurcación en rojo
    for bifurcation in bifurcation_points:
        pop = logistic_map(bifurcation, initial_pop, 1000)
        ax.plot([bifurcation] * last_values, pop[-last_values:], 'ro', markersize=3, label="Bifurcación")

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
    steps = 30  # Cambiar de 10 a 30 para extender el eje x

    population = logistic_map(rate, initial_pop, steps)
    animate_plot()

# Función para actualizar la gráfica de forma animada
def animate_plot(i=0):
    if i == 0:
        ax.clear()
        ax.set_ylim(0, 1)
        ax.set_xlim(0, steps - 1)  # Esto se ajusta automáticamente basado en el valor de steps
        ax.set_xlabel('Tiempo', fontsize=12)
        ax.set_ylabel('Población', fontsize=12)
        ax.set_title('Dinámica de la Población', fontsize=14)
        ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)

    if i < steps:
        ax.plot(range(i + 1), population[:i + 1], marker='o', color='#007acc', linestyle='-', linewidth=2)
        canvas.draw()
        root.after(200, animate_plot, i + 1)

# Función para graficar el Cobweb Plot
def plot_cobweb():
    rate = rate_slider.get()
    initial_pop = initial_pop_slider.get()

    x = np.linspace(0, 1, 500)
    y = rate * x * (1 - x)

    ax.clear()
    ax.plot(x, y, 'r', label=r'$f(x) = r \cdot x \cdot (1 - x)$')
    ax.plot(x, x, 'b', label=r'$y = x$')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Dibujar las líneas del cobweb
    iterations = 10
    current_pop = initial_pop
    for _ in range(iterations):
        next_pop = rate * current_pop * (1 - current_pop)
        ax.plot([current_pop, current_pop], [current_pop, next_pop], 'k', lw=1)
        ax.plot([current_pop, next_pop], [next_pop, next_pop], 'k', lw=1)
        current_pop = next_pop

    ax.set_xlabel('Población actual', fontsize=12)
    ax.set_ylabel('Población siguiente', fontsize=12)
    ax.set_title('Cobweb Plot', fontsize=14)
    ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)
    ax.legend()

    canvas.draw()

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
root.geometry("1300x720")
root.resizable(False, False)  # Desactiva redimensionamiento de la ventana

# Crear un frame contenedor para la gráfica
plot_frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
plot_frame.grid(row=0, column=1, rowspan=9, padx=20, pady=20, sticky="nsew")

# Crear la figura y el eje para la gráfica dentro del frame
fig, ax = plt.subplots(figsize=(10, 7), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Crear un frame para los controles con tamaño fijo
control_frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame", width=300)
control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Bloquear el tamaño del frame de controles
control_frame.grid_propagate(False)

# Configurar sliders, labels y botones con pack o place para mantener el control
ttk.Label(control_frame, text="Tasa de Crecimiento (f)", style="TLabel").pack(fill=tk.X, pady=(0, 10))
rate_slider = ttk.Scale(control_frame, from_=0.0, to=4.0, orient="horizontal")
rate_slider.set(2.0)
rate_slider.pack(fill=tk.X, pady=10)
rate_value_label = ttk.Label(control_frame, text="2.00", style="TLabel")
rate_value_label.pack(fill=tk.X, pady=10)
rate_slider.bind("<Motion>", update_rate)

ttk.Label(control_frame, text="Población Inicial (P0)", style="TLabel").pack(fill=tk.X, pady=(20, 0))
initial_pop_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, orient="horizontal")
initial_pop_slider.set(0.75)
initial_pop_slider.pack(fill=tk.X, pady=10)
initial_pop_value_label = ttk.Label(control_frame, text="0.75", style="TLabel")
initial_pop_value_label.pack(fill=tk.X, pady=10)
initial_pop_slider.bind("<Motion>", update_initial_pop)

play_button = ttk.Button(control_frame, text="Iniciar Animación", command=start_animation, style="TButton")
play_button.pack(fill=tk.X, pady=10)
bifurcation_button = ttk.Button(control_frame, text="Graficar Bifurcación", command=plot_bifurcation, style="TButton")
bifurcation_button.pack(fill=tk.X, pady=10)
bifurcation_label = ttk.Label(control_frame, text="Puntos de bifurcación: N/A", style="TLabel")
bifurcation_label.pack(fill=tk.X, pady=10)
cobweb_button = ttk.Button(control_frame, text="Cobweb Plot", command=plot_cobweb, style="TButton")
cobweb_button.pack(fill=tk.X, pady=10)
clear_button = ttk.Button(control_frame, text="Limpiar Gráfica", command=clear_plot, style="TButton")
clear_button.pack(fill=tk.X, pady=10)
reset_button = ttk.Button(control_frame, text="Resetear Sliders", command=reset_sliders, style="TButton")
reset_button.pack(fill=tk.X, pady=10)

root.mainloop()
