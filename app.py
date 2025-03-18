from PIL import Image, ImageDraw, ImageTk
import tkinter as tk

class App():
    def __init__(self):
        self.IMG_SIZE = 28
        self.DISPLAY_SIZE = 504
        self.SCALE = self.DISPLAY_SIZE // self.IMG_SIZE

        self.root = tk.Tk()
        self.root.title("MNIST")

        self.image = Image.new("L", (self.IMG_SIZE, self.IMG_SIZE), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        self.canvas = tk.Canvas(self.root, width=self.DISPLAY_SIZE, height=self.DISPLAY_SIZE, bg="black")
        self.canvas.pack()

        tk_image = ImageTk.PhotoImage(self.image.resize((self.DISPLAY_SIZE, self.DISPLAY_SIZE), Image.NEAREST))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=tk_image)

        btn_save = tk.Button(self.root, text="Salvar", command=self.save_image)
        btn_save.pack(side=tk.RIGHT, padx=20, pady=10)

        btn_clear = tk.Button(self.root, text="Limpar", command=self.clear_canvas)
        btn_clear.pack(side=tk.LEFT, padx=20,pady=10)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.reset_position)

        self.last_img_coord = (None,None)


    def init_canvas(self):
        pass

    def clear_canvas(self):
        self.image = Image.new("L", (self.IMG_SIZE, self.IMG_SIZE), "black")
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas()

    def get_scaled_coord(self,x,y):
        return (x // self.SCALE,y // self.SCALE)

    def start_draw(self, event):
        self.last_img_coord = self.get_scaled_coord(event.x,event.y)


    def draw_line(self, event):
        print(event.x,event.y,self.get_scaled_coord(event.x,event.y))
        x, y = self.get_scaled_coord(event.x,event.y)
        if self.last_img_coord:
            self.draw.line((*self.last_img_coord, x, y), fill="white", width=1)
            self.last_img_coord = (x,y)
            self.update_canvas()
    
    def update_canvas(self):
        img_resized = self.image.resize((self.DISPLAY_SIZE, self.DISPLAY_SIZE), Image.NEAREST)
        tk_image = ImageTk.PhotoImage(img_resized)
        self.canvas.itemconfig(self.image_on_canvas, image=tk_image)
        self.canvas.image = tk_image

    def reset_position(self, event):
        self.last_img_coord = (None,None)

    def save_image(self):
        self.image.save("mnist_digit.png")
        print("Imagem salva como 'mnist_digit.png'")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
