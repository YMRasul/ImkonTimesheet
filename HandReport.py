from aiogram import types, Router,F
from config import ADMIN,superadmin
from datetime import datetime
from ReportFunc import report1,spis,keldi_ketdi

routerReport = Router()

# отчет по заданой даты drep,2026-02-05
@routerReport.message(F.text.lower().startswith("drep"))
async def cmd_drep(message: types.Message):
    text = message.text
    #result = text.split(',')
    # Разделяем и сразу чистим каждый элемент
    result = [item.strip() for item in text.split(',')]
    current_date = result[1]
    await report1(message, current_date, result[0])
#-------------------------------------------------------
# отчет по текущей даты trep
@routerReport.message(F.text.lower().startswith("trep"))
async def cmd_trep(message: types.Message):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")  # Формат: 2024-05-24
    await report1(message,current_date,message.text[:4])
#---------------------------------------------------------------------
# Список по регистрации
@routerReport.message(F.text.lower().strip().startswith(("spisok","список")))
async def cmd_123(message: types.Message):
    if (message.from_user.id == superadmin or message.from_user.id==ADMIN ):  # Отправим ADMIN у
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")  # Формат: 2024-05-24
        s = f"Список на {current_date}"
        print(s)
        await message.answer(s)
        await spis(message,current_date)
# ---------------Келди кетди--dav---дав-----------------------------------------
@routerReport.message(F.text.lower().strip().startswith(("dav","дав")))
async def cmd_123(message: types.Message):
    text = message.text
    result = [item.strip() for item in text.split(',')]
    if (message.from_user.id == superadmin or message.from_user.id==ADMIN ):  # Отправим ADMIN у
        if len(result) ==2:
            current_date = result[1]
        else:
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")  # Формат: 2024-05-24

        await keldi_ketdi(message,current_date)
# ---------------Келди кетди на любой день-  xdav,2026-02-06--------------------------------
@routerReport.message(F.text.lower().strip().startswith(("xdav","хдав")))
async def cmd_123(message: types.Message):
    if (message.from_user.id == superadmin or message.from_user.id==ADMIN ):  # Отправим ADMIN у
        text = message.text
        result = [item.strip() for item in text.split(',')]
        current_date = result[1]
        await keldi_ketdi(message,current_date)