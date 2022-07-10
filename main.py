import os
import logging
import zipfile

from config import *
from bot_token import TOKEN

from aiogram import Bot, Dispatcher, executor, types

# log
logging.basicConfig(level=logging.INFO)

# initialization bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

list_of_find = []


def file_is_video(file):
    return file.split(".")[1] in extensions_to_sort["C:/Users/HP/Desktop/FILE/VIDEO"]


def check_user_id(user_id):
    return user_id in WHITE_LIST_OF_USER


def find(name, is_file=True):
    list_of_find.clear()

    for root, dirs, files in os.walk("C:/Users"):
        loc = files if is_file else dirs
        for filename in loc:
            if filename.lower() == name.lower():
                file_is_file = True if is_file else False
                list_of_find.append([filename, root, file_is_file])


async def send(file, file_path, is_file=True):
    if is_file:
        if file_is_video(file):
            await bot.send_video(CHAT_ID, open(f"{file_path}/{file}", "rb"))
        else:
            await bot.send_document(CHAT_ID, open(f"{file_path}/{file}", "rb"))
    else:
        os.chdir(file_path)

        z = zipfile.ZipFile(f"{file}_ZIP.zip", "w")
        for root, dirs, files in os.walk(f"{file}"):
            for f in files:
                z.write(os.path.join(root, f))

        z.close()

        await bot.send_document(CHAT_ID, open(f"{file}_ZIP.zip", "rb"))

        os.remove(f"{file}_ZIP.zip")

    list_of_find.clear()


def sort(file_name):
    ex = file_name.split(".")[1]
    for extensions in extensions_to_sort.items():
        if ex in extensions[1]:
            return extensions[0]


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(CHAT_ID, "Команды: \n"
                                    " /get -- получить файл \n"
                                    " /dir -- получить архив директории")


@dp.message_handler(commands=["get"])
async def get_file(message: types.Message):
    if not check_user_id(message.from_user.id):
        await bot.send_message(CHAT_ID, "У вас нет прав для использования бота")
        return

    find(message.text[5:])

    if not list_of_find:
        await message.answer("Такого файла нет((")
        return

    if len(list_of_find) == 1:
        await send(list_of_find[0][0], list_of_find[0][1])
        return

    await bot.send_message(CHAT_ID, f"Обнаружено {len(list_of_find)} файлов, по этим путям: ")
    for i in list_of_find:
        await bot.send_message(CHAT_ID, f"{list_of_find.index(i) + 1} | {i[1]}")

    await bot.send_message(CHAT_ID, "Напишите номер, с нужным путем ")


@dp.message_handler(commands=["dir"])
async def get_dir(message: types.Message):
    if not check_user_id(message.from_user.id):
        await bot.send_message(CHAT_ID, "У вас нет прав для использования бота")
        return

    list_of_find.clear()

    find(message.text[5:], is_file=False)

    if not list_of_find:
        await message.answer("Такой папки нет((")
        return

    if len(list_of_find) == 1:
        await send(list_of_find[0][0], list_of_find[0][1], is_file=False)
        return

    await bot.send_message(CHAT_ID, f"Обнаружено {len(list_of_find)} папок, по этим путям: ")
    for i in list_of_find:
        await bot.send_message(CHAT_ID, f"{list_of_find.index(i) + 1} | {i[1]}")

    await bot.send_message(CHAT_ID, "Напишите номер, с нужным путем ")


@dp.message_handler(content_types=["document"])
async def post_file(message: types.Message):
    file_name = str(message.document.file_name)
    dir_to_save = sort(file_name)
    await message.document.download(destination_dir=f"{dir_to_save}")


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def choose_file(message: types.Message):
    try:
        num = int(message.text) - 1
    except ValueError:
        await bot.send_message(CHAT_ID, "Не верный ввод")
        return

    if not list_of_find:
        await bot.send_message(CHAT_ID, "Запрос еще не задан")
        return

    if num > len(list_of_find) or num < 0:
        await bot.send_message(CHAT_ID, "Данного индекса не существует")
        return

    await send(list_of_find[num][0], list_of_find[num][1], is_file=list_of_find[num][2])


if __name__ == '__main__':
    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)
