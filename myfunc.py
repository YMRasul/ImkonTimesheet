from dbase import Database
from config import PRIX,FORA,ADMIN
from aiogram.types import Message

async def DefUser(bot,message: Message,iduser,idp,dat,tim,minit,minit1,namp,name,dolj):
    #print(message.from_user.full_name)
    print(f"{iduser=},{idp=},{dat=},{tim=} {minit=}")
    if minit < int(PRIX) :     # разница 4 соатдан  кичик булса "Келиш" деб хисоблаймиз
        print(f"Приход {iduser=},{idp=},{dat=},{tim=} {minit=}")
        # проверим если неть запись с признаком prz=0 (пришел)
        # то добавляем запись в таблицу davomad
        tup = (iduser,dat,0)
        async with Database(DBASE) as dbs:

            #INSERT   INTO    davomad(user_id, office_id, data, time, prz, raz)   SELECT ?, ?, ?, ?, ?, ?
            #WHERE    NOT  EXISTS(SELECT 1  FROM davomad  WHERE  user_id = ? AND   data = ? AND   prz = ?  )
            #- Если запись с такими user_id, data  и  prz
            #  уже  есть, блок   SELECT  вернет пустоту, и
            #INSERT не сработает.
            #- Если записи нет, данные из первой строки SELECT  будут  вставлены.

            st = "SELECT * FROM davomad WHERE user_id = ? AND data = ? AND PRZ = ?"
            zp = await dbs.fetch_one(st, tup)  # Данные записи
            if zp is  None:
                sql = '''INSERT INTO davomad (user_id, office_id, data, time, prz,raz)  VALUES (?, ?, ?, ?, ?, ?)'''
                tp = (iduser,idp,dat,tim,0,minit)
                await dbs.IUD(sql, tp)
                sz = f"Келиш белгиланди. {dat}; {tim}"
                await message.answer(sz)
                print(sz + f"{ iduser=},{idp=} Запись келиш в таблицу dovomad произведен.")

                tss = f"{namp}\n{name}\n{dolj}\n{dat}\n{tim}\n"

                if minit > FORA:
                    sv = f"кечикиш {minit} минут."
                    await message.answer(sv)
                    print(sv + f"{ iduser=},{idp=}")
                    tss = tss + sv
                await bot.send_message(chat_id=ADMIN, text=tss)  # Админга хабар
            else:
                print(f"Сиз бир марта {zp[3]}; {zp[4]} да белгиландингиз. {iduser=},{idp=}")
                await message.answer(f"Сиз {zp[3]}; {zp[4]} да келгансиз")
    else:                     # Кетиш
        print(f"Уход {iduser=},{idp=},{dat=},{tim=} {minit1=}")
        tup = (iduser,dat,1)
        async with Database(DBASE) as dbs:
            st = "SELECT * FROM davomad WHERE user_id = ? AND data = ? AND PRZ = ?"
            zp = await dbs.fetch_one(st, tup)  # Данные записи
            if zp:
                # Здесь будет Udate
                print(f"Найдем этой записи и обновим фиксируем новый Уход")
                sql = '''UPDATE davomad SET   time = ?, raz = ?  WHERE user_id = ? AND data = ? AND  prz = ?'''
                tp = (tim,minit1,iduser,dat,1)
                await dbs.IUD(sql, tp)
                sz = f"Кетиш. {dat}; {tim}"
                await message.answer(sz)
                print(sz + f"{ iduser=},{idp=} Новый кетиш в таблицу dovomad произведен.")
            else:
                # Здесь будет Insert
                print(f"Добавим новый запись")
                sql = '''INSERT INTO davomad (user_id, office_id, data, time, prz,raz)  VALUES (?, ?, ?, ?, ?, ?)'''
                tp = (iduser,idp,dat,tim,1,minit1)
                await dbs.IUD(sql, tp)
                sz = f"Кетиш. {dat}; {tim}"
                await message.answer(sz)
                print(sz + f"{ iduser=},{idp=} К в таблицу dovomad произведен.")

