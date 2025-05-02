import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Lista donde se almacenan los artículos
articulos = []

def agregar_articulo():
    nombre = entry_nombre.get()
    peso = entry_peso.get()
    valor = entry_valor.get()
    
    try:
        peso = int(peso)
        valor = int(valor)
        if peso <= 0 or valor <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Peso y valor deben ser enteros positivos.")
        return

    articulos.append({"nombre": nombre, "peso": peso, "valor": valor})
    listbox.insert(tk.END, f"{nombre} | Peso: {peso} | Valor: {valor}")
    entry_nombre.delete(0, tk.END)
    entry_peso.delete(0, tk.END)
    entry_valor.delete(0, tk.END)

def knapsack(items, C):
    N = len(items)
    dp = [[0] * (C + 1) for _ in range(N + 1)]

    for i in range(1, N + 1):
        for c in range(C + 1):
            peso = items[i - 1]["peso"]
            valor = items[i - 1]["valor"]
            if peso <= c:
                dp[i][c] = max(dp[i - 1][c], valor + dp[i - 1][c - peso])
            else:
                dp[i][c] = dp[i - 1][c]

    seleccionados = []
    c = C
    for i in range(N, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            seleccionados.append(items[i - 1])
            c -= items[i - 1]["peso"]

    return seleccionados[::-1], dp[N][C]

def calcular():
    try:
        capacidad = int(entry_capacidad.get())
        if capacidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Capacidad debe ser un entero positivo.")
        return

    if not articulos:
        messagebox.showinfo("Aviso", "Agrega al menos un artículo.")
        return

    seleccionados, valor_total = knapsack(articulos, capacidad)

    resultado = f"Valor total óptimo: ${valor_total}\n"
    resultado += "Artículos seleccionados:\n"
    for item in seleccionados:
        resultado += f"• {item['nombre']} - Peso: {item['peso']}, Valor: {item['valor']}\n"

    messagebox.showinfo("Resultado", resultado)

    # Visualización
    if seleccionados:
        nombres = [item["nombre"] for item in seleccionados]
        valores = [item["valor"] for item in seleccionados]

        plt.figure(figsize=(10, 5))
        plt.barh(nombres, valores, color="teal")
        plt.xlabel("Valor ($)")
        plt.title("Valor económico de artículos seleccionados")
        plt.tight_layout()
        plt.show()

# Interfaz
root = tk.Tk()
root.title("Optimizador de Carga - Knapsack")

tk.Label(root, text="Nombre del artículo:").grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Peso (kg):").grid(row=1, column=0)
entry_peso = tk.Entry(root)
entry_peso.grid(row=1, column=1)

tk.Label(root, text="Valor ($):").grid(row=2, column=0)
entry_valor = tk.Entry(root)
entry_valor.grid(row=2, column=1)

btn_agregar = tk.Button(root, text="Agregar artículo", command=agregar_articulo)
btn_agregar.grid(row=3, column=0, columnspan=2, pady=5)

listbox = tk.Listbox(root, width=50)
listbox.grid(row=4, column=0, columnspan=2, pady=5)

tk.Label(root, text="Capacidad del camión (kg):").grid(row=5, column=0)
entry_capacidad = tk.Entry(root)
entry_capacidad.grid(row=5, column=1)

btn_calcular = tk.Button(root, text="Calcular carga óptima", command=calcular)
btn_calcular.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
