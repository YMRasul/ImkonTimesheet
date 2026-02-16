import os
from aiogram import F, Router, types  # F - это magic фильтр
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,ReplyKeyboardMarkup, KeyboardButton
from dbase import Database
from config import RADIUS,WORKING_START,WORKING_END
from confvar import DBASE
import openpyxl

#-----------------------------------
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from geopy.distance import geodesic
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from myfunc import DefUser
#-----------------------------------
def GetrouterStart(bot):

    routerStart = Router()

    @routerStart.message(CommandStart()) # Хэндлер на команду /start
    async def cmd_start(message: Message):
        await send_phone_request(message) # Поделится номером

        await message.answer(
            "Привет! Нажми на кнопку ниже, чтобы передать свою геопозицию:",
            reply_markup=get_combined_kb()  # Прикрепляем кнопки
    )

    @routerStart.message(F.contact)
    async def get_contact(message: types.Message):
        # логика сохранения-----------------------------------------------
        contact = message.contact
        await saveUser(message,contact)
    #++++++++++++++++++++++++++++++++++++++++++-
    @routerStart.message(F.location)
    async def handle_location(message: Message):
        lat = message.location.latitude
        lon = message.location.longitude
        user = None
        #
        id = message.from_user.id
        async with Database(DBASE) as dbs:
            st = "SELECT * FROM users WHERE user_id = ?"
            user = await dbs.fetch_one(st, (id,))  # Данные офиса

        if user:             # Если наш работник
            user_coords = (lat,lon)
            # Определим локацию офиса из таблицы lat1,lon1
            # pip install geopy
            podr = await idOffice(message)

            lat1 = podr[2]
            lon1 = podr[3]
            radius = podr[4]
            #print(f"id:{podr[0]} nam:{podr[1]} {lat1=} {lon1=} {radius=}")
            office_coords = (lat1,lon1)
            print(f"Координаты {podr[1]} {office_coords}")
            await message.answer(f"Геолокация олинди!")
            print(f"Ваши координаты {user_coords}")
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Расчет в метрах
            distance_meeter = geodesic(user_coords, office_coords).meters
            if distance_meeter < 1000:
                text = f"{podr[1]} дан {distance_meeter:.0f} метр атрофидасиз"
            else:
                text = f"{podr[1]} дан {distance_meeter / 1000:.1f} км атрофидасиз"

            await message.delete() # Убираем карту
            # Зафиксируем приход  до WORKING_END
            # WORKING_START
            rad = int(RADIUS)
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")  # Формат: 2024-05-24
            current_time = now.strftime("%H:%M:%S")  # Формат: 15:30:45

            # Парсим строки в объекты datetime
            fmt = "%H:%M:%S"
            dt1 = datetime.strptime(WORKING_START, fmt)
            dt3 = datetime.strptime(WORKING_END, fmt)

            dt2 = datetime.strptime(current_time, fmt)
            # Вычитаем и получаем разницу в секундах, затем делим на 60
            delta = dt2 - dt1
            delta1= dt2 - dt3
            minutes = delta.total_seconds() / 60
            minutes1 = delta1.total_seconds() / 60

            if  distance_meeter < rad:
                sz = f"Сиз офисдасиз. Вакт {current_time}"
                await message.answer(sz)
                #----------------------------------------------------------------------------------------------------
                await DefUser(bot,message,id,podr[0],current_date,current_time,int(minutes),int(minutes1),podr[1],user[3],user[4] )
                #----------------------------------------------------------------------------------------------------

                print(sz)
                #print(f{int(minutes)} минут кечикдингиз")

            else:
                sz =  f"Хали узокдасиз. Масофа {distance_meeter:.0f} метр"
                print(sz)
                await message.answer(sz)
        else:
            await message.delete() # Убираем карту
            # Если убираем сотрудника из .xlsx файла в users запись остается
            # Чтобы убраь окончательно либо человек должен поделится номером еще раз
            # либо из таблицы users удаляем этой user вручную или придумаем команды типа /del user_id
            sz = f"Сиз руйхатда йуксиз"
            print(sz, f"user_id={id}")
            await message.answer(sz)
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    return routerStart

#---------------------------------------------------------------------------------
async def idOffice(message):
    podr = None
    id = message.from_user.id
    async with Database(DBASE) as dbs:
        st = "SELECT * FROM users WHERE user_id = ?"
        user = await dbs.fetch_one(st, (id,) )  # Данные офиса
        if  user:
            idf = user[5] # Код офиса
            #print(f"User {user[0]} {user[1]} {user[2]} {user[3]} {user[4]}")
            st = "SELECT * FROM offices WHERE id = ?"
            podr = await dbs.fetch_one(st, (idf,))  # Данные офиса
            #print(podr)
            if not podr:
                s = f"Вы не прикреплены в офис. "
                z = f"Офис кодом {idf} нет"
                print(s + z)
                await message.answer(s)
        else:
            s = f"Вас нет в списке. "
            z = f"Нет user в .xlsx файле c {id=}"
            print(s + z )
            await message.answer(s)
    return podr
#------------------------------------------------
async def send_phone_request(message: types.Message):
    # Создаем билдер для клавиатуры
    #builder = ReplyKeyboardBuilder()

    # Вызываем функцию здесь, передавая её результат в reply_markup
    x = get_combined_kb()
    print(f"{x=}")
    await message.answer("Выберите действие:",reply_markup=x )
# ----------------- Функция логики сохранения-----------------------------------------------
async def saveUser(message,contact):
    print(f"{message.from_user.id}  {message.from_user.full_name} {contact.phone_number}")
    # Загружаем файл
    path = os.path.join("xls", "coworkers.xlsx")
    print(f"{path=}")
    wb = openpyxl.load_workbook(path, data_only=True)
    sheet = wb.active
    data = [list(row) for row in sheet.iter_rows(values_only=True)]  # Превращаем строки в список списков
    # Это структура date
    #[
    #    ['TelegramID', 'PhoneNumber', 'FullName', 'Doljnost', 'OfficeID', 'prz', 'date'],
    #    [None, '+998937850078', 'Yusupov Rasuljon Meliboevich', 'IT', 1, 0, datetime.datetime(2025, 12, 24, 0, 0)]
    #]

    #
    row_number = -1  # Значение, если номер не найден
    i = row_number
    for idx, row in enumerate(data, start=1):
        if row[1] == contact.phone_number:
            row_number = idx
            break

    if row_number != -1:
        i = row_number -1
        #print(f"Номер строки в Excel: {i} {data[i][1]} {data[i][2]}")
        idUser       = message.from_user.id
        nameUser     = message.from_user.full_name
        phoneContact = contact.phone_number
        nameXls      = data[i][2]
        doljXls      =data[i][3]
        office_id_Xls=data[i][4]
        przXls       =data[i][5]
        datXls       =data[i][6].strftime('%Y-%m-%d')

        #-------------------------------------------
        tup = (idUser,nameUser,phoneContact,nameXls,doljXls,office_id_Xls,przXls,datXls,)
        print(tup)
        sql = '''INSERT OR REPLACE INTO users (user_id, full_name, phone, name, dolj, office_id, prz, dat) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        async with Database(DBASE) as db:
            await db.IUD(sql,tup)
            await db.conn.commit()
        s1 =  f"Спасибо, {contact.first_name}! Ваш номер {contact.phone_number} получен."
        print(s1)
        #-------------------------------------------
    else:
        s1 =  f"{contact.first_name}! Ваш номер {contact.phone_number} нет в списке"
        print(s1)

        # Удалить из users пользователя  idUser  если такой там есть
        sql = '''DELETE FROM users WHERE user_id = ?'''
        async with Database(DBASE) as db:
            await db.conn.execute("PRAGMA foreign_keys = ON;")
            await db.IUD(sql,(message.from_user.id,))
            await db.conn.commit()

    await message.answer(s1, reply_markup=get_combined_kb())  # не Убираем кнопки
#---------------------------------------------------------
def get_combined_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                # Все три кнопки теперь в одном ряду
                KeyboardButton(text="📱 Регистрация", request_contact=True),
                KeyboardButton(text="🟢 Локация", request_location=True)
            ]
        ],
        resize_keyboard=True, # Это сделает кнопки маленькими и аккуратными
        one_time_keyboard=False
    )
'''
if action == "🟢 Ишга келдим" and current_time > WORK_START:
    time_status = f"⚠️ Кечикди ({current_time})"
    is_violation = True
elif action == "🔴 Ишдан кетдим" and current_time < WORK_END:
    time_status = f"⚠️ Вақли кетди ({current_time})"
    is_violation = True
'''
'''
        #5555555555555555555555555555555
        # Создаем инлайн-кнопки
        #builder = InlineKeyboardBuilder()
        #builder.row(
        #    types.InlineKeyboardButton(text="Келдим", callback_data="status_arrival"),
        #    types.InlineKeyboardButton(text="Кетаяпман", callback_data="status_departure")
        #)

        #await message.answer(text, reply_markup=builder.as_markup()
        #)

        #55555555555555555555555555555555

    #555555555555555555555555555555555555555555555555
    # 2. Обработчики нажатия этих инлайн-кнопок
    @routerStart.callback_query(F.data == "status_arrival")
    async def process_arrival(callback: types.CallbackQuery):
        await callback.message.answer("Зафиксирован приход")
        await callback.answer()  # Обязательно закрываем часики на кнопке

    @routerStart.callback_query(F.data == "status_departure")
    async def process_departure(callback: types.CallbackQuery):
        await callback.message.answer("Зафиксирован уход")
        await callback.answer()
    #555555555555555555555555555555555555555555555555555
'''