"""
Программа для создания изображений и сохранения их в формате *.png.
Графический интерфейс программы разработан на основе TKinter.
"""
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
from tkinter import ttk
from tkinter import simpledialog

from tkinter import Menu


class DrawingApp:
    def __init__(self, root):
        """
        Инициализация __init__(self, root)

        Внутри конструктора выполняются следующие ключевые действия:

        - Устанавливается заголовок окна приложения.
        - Вызывает метод menus_string(), который создает строку меню (Файл, Параметры, Рисование) с раскрывающимся списками;
        - Вызывает метод hot_buttons(), который активирует горячие клавиши некоторых функций;
        - Создается объект изображения (self.image) с использованием библиотеки Pillow. Это изображение служит виртуальным холстом, на котором происходит рисование. Изначально оно заполнено белым цветом.
        - Инициализируется объект ImageDraw.Draw(self.image), который позволяет рисовать на объекте изображения.
        - Создается виджет Canvas Tkinter, который отображает графический интерфейс для рисования. Размеры холста установлены в 600x400 пикселей.
        - Вызывается метод self.setup_ui(), который настраивает элементы управления интерфейса.
        - Привязываются обработчики событий к холсту для отслеживания движений мыши при рисовании (), сброса состояния кисти при отпускании кнопки мыши ().
        - Прописывает цвет кисти по умолчанию;
        - Связывет действия на холсте с функциями: левая кнопка мыши - рисование, правая кнопка мыши - пипетка;

        :param root: Это корневой виджет Tkinter, который служит контейнером для всего интерфейса приложения
        """
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

    def hot_buttons(self) -> None:
        """
        Метод отвечает за настройку горячих клавиш функций графического редактора.
        :return: None
        """
        self.hot_bttn_save = self.root.bind('<Control-s>', self.save_image)
        # self.hot_bttn_save = self.root.bind('<Control-ы>', self.save_image)
        self.hot_bttn_choocol = self.root.bind('<Control-c>', self.choose_color)
        # self.hot_bttn_choocol = self.root.bind('<Control-с>', self.choose_color)

    def menus_string(self) -> None:
        """
        Метод отвечающий за содержание и добавление строки меню в графический интерфейс, для оптимизации рабочего пространства.

        Команда меню "Файл" содержит в себе:

        - кнопку "Сохранить" для сохранения текущего изображения в формате png;

        Команда меню "Параметры" содержит в себе:

        - кнопку "Размер холста" для изменения стандартных ширины и высоты холста;
        - кнопку "Цвет фона", выводящую панель с палитрой для смены цвета фона;

        Команда меню "Рисование" содержит в себе:
        - кнопку "Очистить холст" для полной очистки изображения;

        :return: None
        """
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

    def setup_ui(self) -> None:
        """
        Этот метод отвечает за создание и расположение виджетов управления:

        - Кнопка "Текст" вызывает диалоговое окно для введения текста и вставляет его щелчком мыши в выбранное место;
        - Кнопка "Рисование текстом" позволяет рисовать заданным через диалоговое окно текстом, как кистью;
        - Кнопки "Кисть", "Стёрка" активирует соответствующий режим;
        - Кнопка "Выбрать цвет" для смены стандартного цвета;
        - Окно для отображения текущего цвета;
        - Кнопка вызова метода brushs_size(), при нажатии на которую раскрывается список цифровых значений для изменения толщины инструментов рисования "Кисть" и "Стерка"

        :return: None
        """
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        self.brush_button = tk.Button(self.control_frame, height=2, text="Текст", bg='green', activebackground='grey', command=self.about_txt_add)
        self.brush_button.pack(side=tk.LEFT)

        self.brush_button = tk.Button(self.control_frame, height=2, text="Рисование \n текстом", bg='light green', activebackground='grey', command=self.about_txt)
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

    def canvas_size(self) -> None:
        """
        Метод отвечающий за изменение размера холста.
        Вызывает два диалоговых окна подряд для задания ширины и высоты соответственно.
        Применяет новые параметры к текущему холсту.
        :return: None
        """
        self.width_users_size = tk.simpledialog.askinteger("Параметры холста", prompt="Ширина")
        self.high_users_size = tk.simpledialog.askinteger("Параметры холста", prompt="Высота")
        self.canvas.config(width=self.width_users_size, height=self.high_users_size)



    def about_txt_add(self) -> None:
        """
        :return: None
        """
        self.users_text = simpledialog.askstring("Вставка текста", "Введите текст:")
        self.canvas.bind('<B1-Motion>', self.add_text)

    def add_text(self, event):
        ImageDraw.ImageDraw(self.image).text((event.x, event.y), text=self.users_text, fill=self.pen_color, anchor="ms")


    def about_txt(self) -> None:
        """
        Метод вызывающий диалоговое окно ввода текста.
        Связывает действие левой кнопки мыши на холсте с методом painting_with_text(), отвечающий за рисование текстом.
        :return: None
        """
        self.users_text_brush = simpledialog.askstring("Вставка текста", "Введите текст:")
        self.canvas.bind('<B1-Motion>', self.painting_with_text)

    def painting_with_text(self, event) -> None:
        """
        Сбрасывает последние координаты кисти.
        Рисует на холсте Tkinter и параллельно на объекте Image из Pillow выбранным текстом из метода about_txt(), как обычной кистью, при нажатии ЛКМ.
        :param event:
        :return: None
        """
        self.canvas.create_text(event.x, event.y, text=self.users_text_brush, fill=self.pen_color, font="Verdana 14")
        # ImageDraw.ImageDraw(self.image).text((event.x, event.y), text=self.users_text_brush, fill=self.pen_color)
        # if self.last_x and self.last_y:
        #     self.canvas.create_text(self.last_x, self.last_y, text=self.users_text, fill=self.pen_color)
        #     ImageDraw.ImageDraw(self.image).text((event.x, event.y), text=self.users_text, fill=self.pen_color)
        # self.last_x = event.x
        # self.last_y = event.y

    def background_color(self) -> None:
        """
        Метод отвечающий за изменение цвета фона.
        :return: None
        """
        new_color = colorchooser.askcolor()[1]
        self.canvas.config(background=new_color)
        self.background_color = new_color

    def brush(self) -> None:
        """
        Метод выбора инструмента в качестве рисования на холсте - "Кисть", если он был изменен.
        :return: None
        """
        self.pen_color = 'black'
        self.canvas.bind('<B1-Motion>', self.paint)

    def eraser(self) -> None:
        """
        Метод вызывающий инструмент "Ластик"
        :return: None
        """
        self.pen_color = self.background_color

    def brushs_size(self) -> None:
        """
        Метод, отвечающий за выбор размера кисти/ластика из списка, а так же за список этих размеров
        :return: None
        """
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
        """
        Метод отвечающий за применение выбранного размера к текущему инстркменту
        :param brush_size: размер кисти из списка
        :return: Числовое значение размера кисти
        """
        return self.brush_size.get()

    def paint(self, event) -> None:
        """
        Функция вызывается при движении мыши с нажатой левой кнопкой по холсту.
        Она рисует линии на холсте Tkinter и параллельно на объекте Image из Pillow.
        Линии рисуются между текущей и последней зафиксированной позициями курсора, что создает непрерывное изображение.
        :param event: Событие содержит координаты мыши, которые используются для рисования
        :return: None
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.change_size_brush(self.brush_size), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.change_size_brush(self.brush_size))
        self.last_x = event.x
        self.last_y = event.y

    def pick_color(self, event) -> str:
        """
        Метод отвечающий за перевод формата цвета выбранного пиксела инструмента "Пипетка" из RGB в HEX.
        :param event: Событие содержит строковое значение цвета писксела в формате RGB в координатах нажатия ПКМ на холсте
        :return: Строковое значение цвета в шестнадцатеричном формате (HEX-код)
        """
        rgb_color = self.image.getpixel((event.x, event.y))
        self.pen_color = f'#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}'
        self.label.config(background=self.pen_color)
        return self.pen_color


    def reset(self, event) -> None:
        """
        Сбрасывает последние координаты кисти.
        Это необходимо для корректного начала новой линии после того, как пользователь отпустил кнопку мыши и снова начал рисовать
        :param event: сбрасывает состояние рисования для начала новой линии
        :return:
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self) -> None:
        """
        Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDraw для нового изображения.
        :return:
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, hot_bttn_choocol=None):
        """
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
        :param hot_bttn_choocol:
        :return: Выбранный цвет в диалоговом окне
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.label.config(background=self.pen_color)
        return self.pen_color

    def save_image(self, hot_bttn_save=None) -> None:
        """
        Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
        Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.
        :param hot_bttn_save:
        :return:
        """
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
