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


extensions = {
    "VIDEO": ["mp4", "3g2", "3gp", "3gp2", "3gpp", "3gpp2", "asf", "asx", "avi", "bin", "dat", "drv", "f4v",
              "flv", "gtp", "h264", "m4v", "mkv", "mod", "moov", "mov", "mpeg", "mpg", "mts", "rm", "rmvb",
              "spl", "stl", "swf", "ts", "vcd", "vid", "vob", "webm", "wm", "wmv"],

    "IMG": ["png", "jpg", "jpeg", "raw", "tiff", "psd", "bmp", "gif", "art", "dds", "djvu", "dng", "gbr",
            "gz", "hta", "iff", "iso", "kdc", "mng", "msp", "php", "pot", "pspimage", "scr", "tga", "thm",
            "tif", "vst", "xcf"],

    "TXT": ["txt", "art", "err", "log", "pwi", "sub", "ttf", "tex", "text"],

    "PROGRAM": ["pas", "py", "cpp", "js", "java"],
    "ZIP": ["zip", "rar"],
    "PDF": ["pdf"],

    "MS": ["xlsx", "pptx", "docx"],
}


def find_file(extension):
    for ex in extensions.items():
        if extension in ex[1]:
            return ex[0]


@dp.message_handler(commands=["get"])
async def get_file(message: types.Message):
    global list_of_find_file
    file_input_name = message.text[5:]
    # print(file_input_name)
    file_name, file_ext = str(message.text[5:]).split(".")
    file_dir = find_file(file_ext)
    list_of_find_file = []
    # print(os.getcwd())
    # await bot.send_document(message.chat.id, open("main.py", "rb"))  # <- <- <- <- <- <- <- <-
    # await bot.send_photo(message.chat.id, open("ava.png", "rb"))
    # await bot.send_file(file"txt", file=open("test.txt"))
    for root, dirs, files in os.walk("C:/Users"):
        for filename in files:
            if filename.lower() == file_input_name.lower():
                list_of_find_file.append([filename, root])
                # await message.answer(f"Нашел, вот он: {root}")
                # os.chdir(root)
                # print(os.getcwd())
                # if file_dir == "VIDEO":
                #     await bot.send_video(message.chat.id, open(file_input_name, "rb"))
                # else:
                #     await bot.send_document(message.chat.id, open(file_input_name, "rb"))
                #
                # return

                # match file_dir:
                #     case "VIDEO":
                #         await bot.send_video(message.chat.id, open(file_input_name, "rb"))
                #     case "IMG":
                #         await bot.send_document(message.chat.id, open(file_input_name, "rb"))
                #     case "TXT":
                #         print("TXT")
                #         await bot.send_document(message.chat.id, open(file_input_name, "rb"))
                #     case "PROGRAM":
                #         await bot.send_document(message.chat.id, open(file_input_name, "rb"))
                #     case "ZIP":
                #         await bot.send_document(message.chat.id, open(file_input_name, "rb"))
                #     case "PDF":
                #         await bot.send_document(message.chat.id, open(file_input_name, "rb"))
                #     case "MS":
                #         await bot.send_document(message.chat.id, open(file_input_name, "rb"))
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
    # await AnswerNum.answer.set()
    # await AnswerNum.answer.set()
    # os.chdir(f"C:/Users/HP/Desktop/FILE/{file_dir}")
    # print(os.getcwd())
    # f = open("da.docx")
    # await bot.send_document(message.chat.id, f)
    # with open(r"h.txt", "rb") as doc:
    #     await (doc)
    # f_ = f"{file_name}" + f".{file_ext}"
    # await bot.send_document(message.chat.id, f"{file_name}")
    # f = open(r, "rb")
    # await message.reply_document(open(f"{file_name}.{file_ext}", "rb"))
    # print(f"C:/Users/HP/Desktop/FILE/{file_dir}")
    # print()
    # await bot.send_file(f"{file_name}.{file_ext}")
    # await message.reply_document(open(f"{file_name}.{file_ext}", "rb"))
    # await bot.send_document(message.chat.id, (f"{file_name}.{file_ext}", ))
    print("send")
    # await message.answer()


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





# @dp.message_handler(state=AnswerNum.answer)
# async def get_answer(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["answer"] = message.text
#
#     await AnswerNum.next()
#     await bot.send_message(message.chat.id, "Готова")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
