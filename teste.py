import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Função para lidar com o evento de clique do mouse
def onclick(event):
    ix, iy = event.xdata, event.ydata
    print(f"x = {ix:.2f}, y = {iy:.2f}")

    # Marca o ponto clicado na imagem
    ax.plot(ix, iy, "ro")

    # Anota a coordenada no ponto
    ax.annotate(
        f"({ix:.2f}, {iy:.2f})",
        (ix, iy),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
    )

    # Redesenha o gráfico
    fig.canvas.draw()


# Carregar a imagem
img = mpimg.imread("croqui.png", format="png")

# Criar a figura e os eixos
fig, ax = plt.subplots()

# Mostrar a imagem
ax.imshow(img)

# Conectar o evento de clique do mouse à função
fig.canvas.mpl_connect("button_press_event", onclick)

plt.show()
