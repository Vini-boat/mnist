from PIL import Image, ImageDraw, ImageTk
import tkinter as tk

IMG_SIZE = 28
DISPLAY_SIZE = 500
SCALE = DISPLAY_SIZE // IMG_SIZE

image = Image.new("L", (IMG_SIZE, IMG_SIZE), "black")  # Escala de cinza (L)
draw = ImageDraw.Draw(image)

# Variáveis de controle do mouse
last_x, last_y = None, None

def start_draw(event):
    """Captura o primeiro ponto do desenho."""
    global last_x, last_y
    last_x, last_y = event.x // SCALE, event.y // SCALE  # Ajustar para 28x28

def draw_line(event):
    """Desenha uma linha na imagem reduzida e atualiza a exibição."""
    global last_x, last_y
    x, y = event.x // SCALE, event.y // SCALE  # Ajustar coordenadas
    if last_x is not None and last_y is not None:
        draw.line((last_x, last_y, x, y), fill="white", width=1)  # Desenho na imagem 28x28
        last_x, last_y = x, y
        update_canvas()

def update_canvas():
    """Redimensiona a imagem e atualiza o Canvas."""
    img_resized = image.resize((DISPLAY_SIZE, DISPLAY_SIZE), Image.NEAREST)  # Escalar sem suavizar
    tk_image = ImageTk.PhotoImage(img_resized)
    canvas.itemconfig(image_on_canvas, image=tk_image)
    canvas.image = tk_image  # Evita garbage collector

def reset_position(event):
    """Reseta a posição do mouse ao soltar o botão."""
    global last_x, last_y
    last_x, last_y = None, None

def save_image():
    """Salva a imagem em 28x28 pixels."""
    image.save("mnist_digit.png")
    print("Imagem salva como 'mnist_digit.png'")

# Criar janela Tkinter
root = tk.Tk()
root.title("Desenho MNIST")

# Criar Canvas
canvas = tk.Canvas(root, width=DISPLAY_SIZE, height=DISPLAY_SIZE, bg="white")
canvas.pack()

# Adicionar imagem ao Canvas
tk_image = ImageTk.PhotoImage(image.resize((DISPLAY_SIZE, DISPLAY_SIZE), Image.NEAREST))
image_on_canvas = canvas.create_image(0, 0, anchor="nw", image=tk_image)

# Botão para salvar
btn_save = tk.Button(root, text="Salvar", command=save_image)
btn_save.pack()

# Associar eventos do mouse
canvas.bind("<Button-1>", start_draw)       # Clique inicial
canvas.bind("<B1-Motion>", draw_line)       # Arrastar para desenhar
canvas.bind("<ButtonRelease-1>", reset_position)  # Soltar botão do mouse

root.mainloop()
