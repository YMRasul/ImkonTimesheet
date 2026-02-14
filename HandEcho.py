from aiogram import Router, types

# Создаем роутер
routerEcho = Router()

@routerEcho.message()
async def echo_handler(message: types.Message):
    await message.copy_to(chat_id=message.chat.id)
