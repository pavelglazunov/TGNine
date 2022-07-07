from config import *
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

list_of_find_file = []


class AnswerNum(StatesGroup):
    answer = State()


def find_file(extension):
    for ex in extensions.items():
        if extension in ex[1]:
            return ex[0]


@dp.message_handler(commands=["get"])
async def get_file(message: types.Message):
    global list_of_find_file
    file_input_name = message.text[5:]
    file_name, file_ext = str(message.text[5:]).split(".")
    file_dir = find_file(file_ext)
    list_of_find_file = []

    for root, dirs, files in os.walk("C:/Users"):
        for filename in files:
            if filename.lower() == file_input_name.lower():
                list_of_find_file.append([filename, root])

    if not list_of_find_file:
        await message.answer("Такого файла нет((")
        return

    if len(list_of_find_file) == 1:
        if file_dir == "VIDEO":
            await bot.send_video(message.chat.id, open(f"{list_of_find_file[0][1]}/{list_of_find_file[0][0]}", "rb"))
        else:
            await bot.send_document(message.chat.id, open(f"{list_of_find_file[0][1]}/{list_of_find_file[0][0]}", "rb"))
        return

    await bot.send_message(message.chat.id, f"Обнаружено {len(list_of_find_file)} файлов, по этим путям: ")
    for i in list_of_find_file:
        await bot.send_message(message.chat.id, f"{list_of_find_file.index(i) + 1} | {i[1]}")

    await bot.send_message(message.chat.id, "Напишите номер, с нужным путем ")


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_file(message: types.Message):
    global list_of_find_file

    try:
        num = int(message.text) - 1
    except ValueError:
        await bot.send_message(message.chat.id, "Не верный ввод")
        return

    if not list_of_find_file:
        await bot.send_message(message.chat.id, "Запрос еще не задан")
        return

    if num > len(list_of_find_file) or num < 0:
        await bot.send_message(message.chat.id, "Данного индекса не существует")
        return

    await bot.send_document(message.chat.id, open(f"{list_of_find_file[num][1]}/{list_of_find_file[num][0]}", "rb"))
    list_of_find_file = []


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
