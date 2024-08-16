# 🔬 Simulador de Dinámica Poblacional: Modelo Logístico

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![tkinter](https://img.shields.io/badge/tkinter-included-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![NumPy](https://img.shields.io/badge/NumPy-1.19+-yellow.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.3+-orange.svg)](https://matplotlib.org/)

## 📊 Descripción del Proyecto

Este proyecto implementa un simulador interactivo basado en el modelo logístico de dinámica poblacional. La población se modela utilizando la fórmula:

$P_{n+1} = f \times P_n \times (1 - P_n)$

Donde:
- $P_n \in [0, 1]$ representa el porcentaje de la población existente en el año $n$ con respecto al máximo.
- $f \in [0, 4]$ es la constante de fertilidad y representa la tasa de crecimiento de la población.

## 🎓 Comportamiento del Modelo

El comportamiento de la población varía según el valor de la constante de fertilidad $f$:

- Para $0 \le f \le 1$: La población eventualmente muere (0 bifurcaciones).
- Para $1 < f < 2$: La población se estabiliza (1 bifurcación).
- Para ciertos valores de $f$: La población oscila entre dos valores (2 bifurcaciones).
- Para otros valores de $f$: Se observan comportamientos más complejos y múltiples bifurcaciones.

## 🎯 Objetivos del Proyecto

1. Investigar sobre puntos fijos e iteración funcional.
2. Determinar la expresión matemática del valor de convergencia para $1 \le f \le 2$.
3. Calcular el número de bifurcaciones para todos los valores de $f \ge 0$.
4. Analizar el comportamiento de la población para diversos valores de $f$ y $P_0$.
5. Implementar un programa en Python que:
   - Incluya controles deslizantes para $f$ y $P_0$.
   - Grafique la evolución de la población en función del tiempo.
   - Muestre el diagrama de bifurcación en función de $f$.

![Simulador de Dinámica Poblacional](assets/poblacion.gif)

## ✨ Características del Simulador

- 📉 Visualización en tiempo real de la dinámica poblacional
- 🔀 Generación de diagramas de bifurcación
- 🎛️ Controles interactivos para ajustar $f$ y $P_0$
- ▶️ Animación del crecimiento poblacional
- 🔄 Opciones para reiniciar y limpiar gráficos

## 🛠️ Requisitos

- Python 3.7+
- tkinter (generalmente incluido con Python)
- NumPy
- Matplotlib

## 🚀 Instalación

1. Clona este repositorio:
