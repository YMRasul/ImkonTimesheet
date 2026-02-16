from aiogram import Router,F
from config import superadmin,DBASE
from aiogram.filters import Command
#----------------------------
routerHelp = Router()
#----------------------------
@routerHelp.message(Command('help'))
async def copybase(message):
    hlp = ''
    if message.from_user.id == superadmin:  # superUser
        hlp = hlp + "\n/copybase\n/copyxls\n/copylog\n/droplog\n/copyconf"
        hlp = hlp + "\ndav"
        hlp = hlp + "\nxdav,YYYY-MM-DD"
        hlp = hlp + "\nspisok"
        hlp = hlp + "\ndrep,YYYY-MM-DD"
        hlp = hlp + "\ntrep"
    await message.answer(hlp)
