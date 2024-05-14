import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.background_color = 'white'
        self.canvas = tk.Canvas(root, width=600, height=400, bg=self.background_color)
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Button-3>', self.pick_color)

        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        clear_button = tk.Button(self.control_frame, height=2, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        self.brush_button = tk.Button(self.control_frame, height=2, text="Кисть", bg='pink', activebackground='grey', command=self.brush)
        self.brush_button.pack(side=tk.LEFT)


        color_button = tk.Button(self.control_frame, height=2, text="Выбрать \n цвет", bg='light blue', activebackground='grey', command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(self.control_frame, height=2, text="Стёрка", bg='white', activebackground='grey', command=self.eraser)
        self.eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(self.control_frame, height=2, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brushs_size()

    def brush(self):
        self.pen_color = 'black'

    def eraser(self):
        self.pen_color = self.background_color

    def brushs_size(self) -> None:
        sizes = [brush for brush in range(1, 11)]
        self.brush_size = tk.IntVar(self.root)
        self.brush_size.set(sizes[0])
        self.list_size_brush_button = tk.OptionMenu(
            self.control_frame,
            self.brush_size,
            *sizes,
            command=self.change_size_brush
        )
        self.list_size_brush_button.pack(side=tk.LEFT)

    def change_size_brush(self, brush_size) -> int:
        return self.brush_size.get()

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.change_size_brush(self.brush_size), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.change_size_brush(self.brush_size))
        self.last_x = event.x
        self.last_y = event.y

    def pick_color(self, event):
        rgb_color = self.image.getpixel((event.x, event.y))
        self.pen_color = f'#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}'
        return self.pen_color


    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
