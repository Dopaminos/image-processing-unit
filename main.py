import argparse
from tkinter import Tk
from image_editor_app import ImageEditorApp

def parse_arguments():
    parser = argparse.ArgumentParser(description="Image Processing Application")
    parser.add_argument('--filter', type=int, default=0, help='Filter to apply (0 = None, 1 = Negative, etc.)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    root = Tk()
    filter_map = {
        0: "Нет",
        1: "Негатив",
        2: "Степенное преобразование",
        3: "Вырезание диапазона яркостей",
        4: "Линейный сглаживающий фильтр",
        5: "Медианный фильтр",
        6: "Градиент Робертса",
        7: "Градиент Собеля",
        8: "Лапласиан",
        9: "Гистограмма изображения",
        10: "Эквализация гистограммы",
        11: "Пороговый фильтр с глобальным порогом",
        12: "Пороговый фильтр методом Оцу",
        13: "Морфология: Дилатация",
        14: "Морфология: Эрозия",
        15: "Морфология: Замыкание",
        16: "Морфология: Размыкание",
        17: "Морфология: Выделение границ",
        18: "Морфология: Остов"
    }
    selected_filter = filter_map.get(args.filter, "Нет")
    app = ImageEditorApp(root, default_filter=selected_filter)
    root.mainloop()

if __name__ == "__main__":
    main()
