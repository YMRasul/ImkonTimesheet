from aiogram import Router,F
from config import superadmin,DBASE,PATH1,XLS,ADMIN,CNF
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram import types
from dbase import Database
#-------------------------------------------------------------------
routerAdmin = Router()

def GetRouterAdmin(bot):

    routerAdmin = Router()

    #-------------  Копирование базу данных -----------------------------
    @routerAdmin.message(Command('copybase'))   # Копирование базу данных
    async def copybase(message):
        if message.from_user.id == superadmin:  # superUser
            src = DBASE
            print(f'{DBASE=}')
            file = FSInputFile(src)              # Загружаем файл
            await message.answer_document(file)  # Отправляем файл
    #---------------Сохранить файл-----------------------------------------
    @routerAdmin.message(F.document)
    async def handle_document(message: types.Message, bot: bot):
        # Получаем объект документа
        file_id = message.document.file_id
        file_name = message.document.file_name  # Оригинальное имя файла
        result = (file_name.split('.')[1]).upper()
        if message.from_user.id == superadmin  or message.from_user.id == ADMIN:  # superUser
            if message.from_user.id == superadmin:
                if file_name == 'config.py':
                    # Скачиваем в текущую директорию
                    path = file_name
                    print(f"{path=} {result}")
                    await bot.download(
                        file=file_id,
                        destination=path  # Файл сохранится с оригинальным именем в папке PATH1
                    )
                    await message.answer(f"Файл {file_name} сохранен!")
            if result=='XLSX':
                # Скачиваем в текущую директорию
                path = PATH1 + file_name
                print(f"{path=} {result}")
                await bot.download(
                    file=file_id,
                    destination = path  # Файл сохранится с оригинальным именем в папке PATH1
                )
                await message.answer(f"Файл {file_name} сохранен!")
        else:
            await message.answer(f"Вы не ADMIN")

    #-------------  Копирование XLSX -----------------------------
    @routerAdmin.message(Command('copyxls'))   # Копирование базу данных
    async def copybase(message):
        if message.from_user.id == superadmin  or message.from_user.id == ADMIN:  # superUser
            src = XLS
            print(f'{src=}')
            file = FSInputFile(src)              # Загружаем файл
            await message.answer_document(file)  # Отправляем файл
        else:
            await message.answer(f"Вы не ADMIN")
    #-------------  Копирование XLSX -----------------------------
    @routerAdmin.message(Command('copyconf'))   # Копирование
    async def copybase(message):
        if message.from_user.id == superadmin  or message.from_user.id == ADMIN:  # superUser
            src = CNF
            print(f'{src=}')
            file = FSInputFile(src)              # Загружаем файл
            await message.answer_document(file)  # Отправляем файл
        else:
            await message.answer(f"Вы не ADMIN")

    return routerAdmin

