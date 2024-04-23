#pylint: disable=all

import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import tkinter as tk
from tkinter import simpledialog


quadrados_selecionados = []


def gerar_quadrados(largura, altura):
    quadrados = []
    nome_sequencia = 1
    for x in range(largura):
        for y in range(altura):
            nome = f"{nome_sequencia:02d}"
            quadrado = Polygon([(x, y), (x+1, y), (x+1, y+1), (x, y+1)])
            cor = "green" if (x + y) % 2 == 0 else "lightgreen"
            quadrados.append({"quadrado": quadrado, "nome": nome, "cor": cor})
            nome_sequencia += 1
    return quadrados


def abrir_dialogo():
    root = tk.Tk()
    root.withdraw()
    produto = simpledialog.askstring("Informação do Produto", "Digite o nome do produto:")
    codigo = simpledialog.askstring("Informação do Produto", "Digite o código do produto:")
    andar = simpledialog.askstring("Informação do Produto", "Digite o andar do produto:")
    root.destroy()
    if produto and codigo and andar:
        return {"produto": produto, "codigo": codigo, "andar": andar}
    return None



def on_click(event):
    x_click = event.xdata
    y_click = event.ydata
    if x_click is None or y_click is None:
        return

    for quadrado_info in quadrados:
        quadrado = quadrado_info["quadrado"]
        artista = quadrado_info["artista"]
        if quadrado.contains(Point(x_click, y_click)):
            if quadrado_info.get("selecionado", False):
                quadrado_info["selecionado"] = False
                artista.set_facecolor(quadrado_info["cor"])
                artista.set_alpha(0.2)
                if quadrado_info["nome"] in quadrados_selecionados:
                    quadrados_selecionados.remove(quadrado_info["nome"])
                if "produto_info" in quadrado_info:
                    del quadrado_info["produto_info"]
            else:
                info_produto = abrir_dialogo()
                if info_produto:
                    quadrado_info["selecionado"] = True
                    artista.set_facecolor('blue')
                    artista.set_alpha(0.5)
                    quadrado_info["produto_info"] = info_produto
                    quadrados_selecionados.append(quadrado_info["nome"])
            break
    plt.draw()
    print("Quadrados selecionados:", quadrados_selecionados)


plano_estoque = Polygon([(0, 0), (30, 0), (30, 20), (0, 20)])
quadrados = gerar_quadrados(30, 20)

fig, ax = plt.subplots(figsize=(15, 10))
x, y = plano_estoque.exterior.xy
ax.plot(x, y, marker='o')
ax.fill(x, y, alpha=0.2, color='lightgrey')

for quadrado in quadrados:
    x, y = quadrado["quadrado"].exterior.xy
    patch = ax.fill(x, y, color=quadrado["cor"], alpha=0.1)[0]  # [0] para pegar o primeiro artista
    quadrado["artista"] = patch  # Guardar a referência ao artista
    centroide = quadrado["quadrado"].centroid
    ax.text(centroide.x, centroide.y, quadrado["nome"],
            horizontalalignment='center', verticalalignment='center',
            fontsize=8, color='darkblue')

# Definindo as estantes como polígonos menores dentro do plano
estantes_v = [
    {"poligono": Polygon([(2, 2), (4, 2), (4, 18), (2, 18)]), "nome": "1", "cor": "red"},
    {"poligono": Polygon([(6, 2), (8, 2), (8, 18), (6, 18)]), "nome": "2", "cor": "red"},
    {"poligono": Polygon([(10, 2), (12, 2), (12, 18), (10, 18)]), "nome": "3",  "cor": "red"},
    {"poligono": Polygon([(14, 2), (16, 2), (16, 18), (14, 18)]), "nome": "4",  "cor": "red"},
]

estantes_h = [
    {"poligono": Polygon([(18, 4), (28, 4), (28, 6), (18, 6)]), "nome": "5",  "cor": "red"},
    {"poligono": Polygon([(18, 8), (28, 8), (28, 10), (18, 10)]), "nome": "6",  "cor": "red"},
    {"poligono": Polygon([(18, 12), (28, 12), (28, 14), (18, 14)]), "nome": "7",  "cor": "red"},
    {"poligono": Polygon([(18, 16), (28, 16), (28, 18), (18, 18)]), "nome": "8",  "cor": "red"},
]

# Desenhando e nomeando cada estante
for estante in estantes_v:
    x, y = estante["poligono"].exterior.xy
    plt.plot(x, y, color=estante["cor"], marker='o')
    plt.fill(x, y, color=estante["cor"], alpha=0.5)  # Pode alterar a cor se desejar distinguir as estantes

    # Calculando o centroide da estante para posicionar o nome
    centroide = estante["poligono"].centroid
    plt.text(
        centroide.x, 
        centroide.y, 
        f'Estante {estante["nome"]}',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=90
    )

for estante in estantes_h:
    x, y = estante["poligono"].exterior.xy
    plt.plot(x, y, color=estante["cor"], marker='o')
    plt.fill(x, y, color=estante["cor"], alpha=0.5)  # Pode alterar a cor se desejar distinguir as estantes

    # Calculando o centroide da estante para posicionar o nome
    centroide = estante["poligono"].centroid
    plt.text(
        centroide.x, 
        centroide.y, 
        f'Estante {estante["nome"]}',
        horizontalalignment='center',
        verticalalignment='center'
    )

fig.canvas.mpl_connect('button_press_event', on_click)

ax.set_title("Planta Baixa do Estoque - Plano 30x20 com Quadrantes Numerados")
ax.set_xlim(0, 31)
ax.set_ylim(0, 21)
ax.set_xlabel("Comprimento (m)")
ax.set_ylabel("Largura (m)")
ax.set_xticks(range(0, 31, 1))
ax.set_yticks(range(0, 21, 1))
ax.grid(True)
ax.set_aspect('equal', adjustable='box')

plt.show()
