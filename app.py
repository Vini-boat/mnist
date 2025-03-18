from PIL import Image, ImageDraw, ImageTk
import tkinter as tk

class App():
    def __init__(self):
        self.IMG_SIZE = 28
        self.DISPLAY_SIZE = 500
        self.SCALE = self.DISPLAY_SIZE // self.IMG_SIZE

        self.image = Image.new("L", (self.IMG_SIZE, self.IMG_SIZE), "black")  # Escala de cinza (L)
        
        self.draw = ImageDraw.Draw(self.image)
        self.root = tk.Tk()
        self.root.title("Desenho MNIST")
        
        self.canvas = tk.Canvas(self.root, width=self.DISPLAY_SIZE, height=self.DISPLAY_SIZE, bg="black")
        self.canvas.pack()

        tk_image = ImageTk.PhotoImage(self.image.resize((self.DISPLAY_SIZE, self.DISPLAY_SIZE), Image.NEAREST))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=tk_image)

        btn_save = tk.Button(self.root, text="Salvar", command=self.save_image)
        btn_save.pack()

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.reset_position)

        self.last_x = None
        self.lasy_y = None

    def start_draw(self, event):
        self.last_x, self.last_y = event.x // self.SCALE, event.y // self.SCALE
    
    def draw_line(self, event):
        x, y = event.x // self.SCALE, event.y // self.SCALE
        if self.last_x and self.last_y:
            self.draw.line((self.last_x, self.last_y, x, y), fill="white", width=1)
            self.last_x, self.last_y = x, y
            self.update_canvas()
    
    def update_canvas(self):
        img_resized = self.image.resize((self.DISPLAY_SIZE, self.DISPLAY_SIZE), Image.NEAREST)
        tk_image = ImageTk.PhotoImage(img_resized)
        self.canvas.itemconfig(self.image_on_canvas, image=tk_image)
        self.canvas.image = tk_image

    def reset_position(self, event):
        self.last_x, self.last_y = None, None

    def save_image(self):
        self.image.save("mnist_digit.png")
        print("Imagem salva como 'mnist_digit.png'")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
