import cv2
import numpy as np
from tkinter import Tk, filedialog, Label, ttk, HORIZONTAL
from PIL import Image, ImageTk
from ttkbootstrap import Style
from image_processor import ImageProcessor

class ImageEditorApp:
    def __init__(self, master, default_filter="Нет"):
        self.master = master
        self.processor = ImageProcessor()
        self.default_filter = default_filter
        self.original_image = None
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Редактор изображений")
        screen_height = self.master.winfo_screenheight()
        window_height = int(screen_height * 0.8)
        self.master.geometry(f"1200x{window_height}")

        style = Style("darkly")

        self.image_frame = ttk.Frame(self.master)
        self.image_frame.pack(side="left", fill="both", expand=True)

        self.control_frame = ttk.Frame(self.master, padding=10)
        self.control_frame.pack(side="right", fill="y")

        self.image_label = Label(self.image_frame, background="black")
        self.image_label.pack(fill="both", expand=True)

        open_button = ttk.Button(self.control_frame, text="Открыть изображение", command=self.open_image)
        open_button.pack(pady=10)

        self.filter_combobox = ttk.Combobox(self.control_frame, state="readonly")
        self.update_filter_options()
        self.filter_combobox.set(self.default_filter)
        self.filter_combobox.pack(pady=10)

        self.slider = ttk.Scale(self.control_frame, from_=1, to=10, orient=HORIZONTAL, command=self.apply_filter)
        self.slider.pack(pady=10)
        self.slider.pack_forget()  # скрываем слайдер по умолчанию

        self.save_button = ttk.Button(self.control_frame, text="Сохранить изображение", command=self.save_image)
        self.save_button.pack(pady=10)

        self.filter_combobox.bind("<<ComboboxSelected>>", self.update_slider_and_apply_filter)

    def update_filter_options(self):
        filters = [
            "Нет", "Негатив", "Степенное преобразование", "Вырезание диапазона яркостей",
            "Линейный сглаживающий фильтр", "Медианный фильтр", "Градиент Робертса",
            "Градиент Собеля", "Лапласиан", "Гистограмма изображения", "Эквализация гистограммы",
            "Пороговый фильтр с глобальным порогом", "Пороговый фильтр методом Оцу",
            "Морфология: Дилатация", "Морфология: Эрозия", "Морфология: Замыкание",
            "Морфология: Размыкание", "Морфология: Выделение границ", "Морфология: Остов"
        ]
        if self.default_filter == "Нет":
            self.filter_combobox['values'] = filters
        else:
            self.filter_combobox['values'] = ["Нет", self.default_filter]

    def update_slider_and_apply_filter(self, event):
        filter_name = self.filter_combobox.get()
        if filter_name == "Негатив":
            self.slider.pack_forget()
        elif filter_name in ["Степенное преобразование", "Вырезание диапазона яркостей", "Линейный сглаживающий фильтр", "Медианный фильтр", "Пороговый фильтр с глобальным порогом"]:
            self.slider.pack(pady=10)
        else:
            self.slider.pack_forget()

        self.apply_filter()

    def save_image(self):
        if self.processor.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                       filetypes=[("PNG files", "*.png"),
                                                                  ("JPEG files", "*.jpg;*.jpeg"),
                                                                  ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.processor.processed_image)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.processor.load_image(file_path)
            self.original_image = self.processor.current_image.copy()
            self.resize_and_show_image(self.processor.current_image)

    def resize_and_show_image(self, img):
        height, width = img.shape[:2]
        scale = min(self.image_frame.winfo_height() / height, self.image_frame.winfo_width() / width)
        resized_img = cv2.resize(img, (int(width * scale), int(height * scale)))
        img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def apply_filter(self, *args):
        filter_name = self.filter_combobox.get()
        if filter_name == "Нет":
            self.processor.current_image = self.original_image.copy()
            self.processor.processed_image = self.original_image.copy()
        elif filter_name == "Негатив":
            self.processor.apply_negative()
        elif filter_name == "Степенное преобразование":
            self.processor.apply_power_transform(self.slider.get())
        elif filter_name == "Вырезание диапазона яркостей":
            self.processor.apply_brightness_cut(50, self.slider.get())
        elif filter_name == "Линейный сглаживающий фильтр":
            self.processor.apply_smoothing_filter(int(self.slider.get()))
        elif filter_name == "Медианный фильтр":
            self.processor.apply_median_filter(int(self.slider.get()))
        elif filter_name == "Градиент Робертса":
            self.processor.apply_roberts()
        elif filter_name == "Градиент Собеля":
            self.processor.apply_sobel()
        elif filter_name == "Лапласиан":
            self.processor.apply_laplacian()
        elif filter_name == "Гистограмма изображения":
            self.processor.apply_histogram()
        elif filter_name == "Эквализация гистограммы":
            self.processor.apply_hist_equalization()
        elif filter_name == "Пороговый фильтр с глобальным порогом":
            self.processor.apply_threshold_global(int(self.slider.get()))
        elif filter_name == "Пороговый фильтр методом Оцу":
            self.processor.apply_threshold_otsu()
        elif filter_name == "Морфология: Дилатация":
            self.processor.apply_dilation()
        elif filter_name == "Морфология: Эрозия":
            self.processor.apply_erosion()
        elif filter_name == "Морфология: Замыкание":
            self.processor.apply_closing()
        elif filter_name == "Морфология: Размыкание":
            self.processor.apply_opening()
        elif filter_name == "Морфология: Выделение границ":
            self.processor.apply_boundary_extraction()
        elif filter_name == "Морфология: Остов":
            self.processor.apply_skeletonization()

        self.resize_and_show_image(self.processor.processed_image)
