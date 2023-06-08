import asyncio
import os
from tkinter import filedialog

from editor import ImageEditor
from utils import get_image_paths


async def main():
    cls()
    input("Выберите папку с фотками. \nНажмите клавишу Enter чтобы продолжить.")
    in_folder = filedialog.askdirectory()

    cls()
    input("Выберите папку куда сохранить результат. \nНажмите клавишу Enter чтобы продолжить.")
    out_folder = filedialog.askdirectory()

    editor = ImageEditor(
        get_image_paths(in_folder),
        out_folder
    )

    cls()
    print(f"Папка с фото: {in_folder}\n"
          f"Папка для результатов: {out_folder}\n\n")

    print("Выберите действие:\n"
          "\t1. Добавить лого\n"
          "\t2. Переименовать\n"
          "\t3. Добавить лого и переименовать\n")

    is_choosing = True
    while is_choosing:
        action = input("--> ")

        match action:
            case "1":
                await editor.add_logo()

            case "2":
                cls()
                new_name = input("Введите новое имя: ")

                await editor.rename_images(new_name)

            case "3":
                cls()
                new_name = input("Введите новое имя: ")

                await editor.add_logo()

                editor.reinit(get_image_paths(out_folder), out_folder)

                await editor.clean_out_folder()
                await editor.restore_buffered_images(new_name)

            case _:
                cls()
                print("Неверная опция! Попробуйте опять\n")
                print("Выберите действие:\n"
                      "\t1. Добавить лого\n"
                      "\t2. Переименовать\n"
                      "\t3. Добавить лого и переименовать\n")

                continue
        cls()

        is_choosing = False
        print("Операция успешно выполнена!")


def cls():
    os.system("cls")


asyncio.run(main())
