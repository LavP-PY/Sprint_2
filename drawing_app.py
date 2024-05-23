import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
from tkinter import ttk
from tkinter import simpledialog

from tkinter import Menu


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.menus_string()

        self.hot_buttons()

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

        self.label.config(background=self.pen_color)

    def hot_buttons(self):
        self.hot_bttn_save = self.root.bind('<Control-s>', self.save_image)
        # self.hot_bttn_save = self.root.bind('<Control-ы>', self.save_image)
        self.hot_bttn_choocol = self.root.bind('<Control-c>', self.choose_color)
        # self.hot_bttn_choocol = self.root.bind('<Control-с>', self.choose_color)

    def menus_string(self):
        mainmenu = Menu(self.root)
        self.root.config(menu=mainmenu)

        file_menu = Menu(mainmenu, tearoff=0)
        file_menu.add_command(label="Сохранить как...", command=self.save_image)

        paramets_menu = Menu(mainmenu, tearoff=0)
        paramets_menu.add_command(label="Размер холста", command=self.canvas_size)
        paramets_menu.add_command(label="Цвет фона", command=self.background_color)

        painting_menu = Menu(mainmenu, tearoff=0)
        painting_menu.add_command(label="Очистить холст", command=self.clear_canvas)

        mainmenu.add_cascade(label="Файл", menu=file_menu)
        mainmenu.add_cascade(label="Параметры", menu=paramets_menu)
        mainmenu.add_cascade(label="Рисование", menu=painting_menu)

    def setup_ui(self):
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        # save_button = tk.Button(self.control_frame, height=2, text="Сохранить", command=self.save_image)
        # save_button.pack(side=tk.LEFT)

        # clear_button = tk.Button(self.control_frame, height=2, text="Очистить", command=self.clear_canvas)
        # clear_button.pack(side=tk.LEFT)

        self.brush_button = tk.Button(self.control_frame, height=2, text="Текст", bg='light green', activebackground='grey', command=self.about_txt)
        self.brush_button.pack(side=tk.LEFT)

        self.brush_button = tk.Button(self.control_frame, height=2, text="Кисть", bg='pink', activebackground='grey', command=self.brush)
        self.brush_button.pack(side=tk.LEFT)

        self.label = ttk.Label(self.control_frame, width=2)
        self.label.pack(side=tk.LEFT)

        color_button = tk.Button(self.control_frame, height=2, text="Выбрать \n цвет", bg='light blue', activebackground='grey', command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(self.control_frame, height=2, text="Стёрка", bg='white', activebackground='grey', command=self.eraser)
        self.eraser_button.pack(side=tk.LEFT)

        self.brushs_size()

    def canvas_size(self):
        self.width_users_size = tk.simpledialog.askinteger("Параметры холста", prompt="Ширина")
        self.high_users_size = tk.simpledialog.askinteger("Параметры холста", prompt="Высота")
        self.canvas.config(width=self.width_users_size, height=self.high_users_size)

    def about_txt(self):
        self.users_text = simpledialog.askstring("Вставка текста", "Введите текст:")
        self.canvas.bind('<B1-Motion>', self.add_text)
    def add_text(self, event):
        self.canvas.create_text(event.x, event.y, text=self.users_text, fill=self.pen_color, font="Verdana 14")
        ImageDraw.ImageDraw(self.image).text((event.x, event.y), text=self.users_text, fill=self.pen_color)
        # if self.last_x and self.last_y:
        #     self.canvas.create_text(self.last_x, self.last_y, text=self.users_text, fill=self.pen_color)
        #     ImageDraw.ImageDraw(self.image).text((event.x, event.y), text=self.users_text, fill=self.pen_color)
        # self.last_x = event.x
        # self.last_y = event.y

    def background_color(self):
        new_color = colorchooser.askcolor()[1]
        self.canvas.config(background=new_color)
        self.background_color = new_color

    def brush(self):
        self.pen_color = 'black'
        self.canvas.bind('<B1-Motion>', self.paint)

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
        print(self.pen_color, type(self.pen_color))
        self.label.config(background=self.pen_color)
        return self.pen_color


    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, hot_bttn_choocol=None):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.label.config(background=self.pen_color)
        return self.pen_color
        # print(self.pen_color, type(self.pen_color))

    def save_image(self, hot_bttn_save=None):
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
