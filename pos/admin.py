from django.contrib import admin
from . import models
# from . import Bot1
from aiogram.types import Message
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
import asyncio

# Register your models here.

import logging
from django.contrib.auth.models import User
from pos.models import Chel
from aiogram.client import bot
from aiogram import Dispatcher
from aiogram import types
# from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from .tokid import toki, idVo
# from asgiref.sync import sync_to_async
# from asgiref.sync import async_to_sync
from threading import Thread

logging.basicConfig(level=logging.INFO)

bot1 = bot.Bot(token=toki)
dp = Dispatcher()


@dp.startup()
async def start():
    await bot1.send_message(idVo, 'Поехали!')


@async_to_sync()
async def m(tgid, tex):
    await bot1.send_message(tgid, tex)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await  message.answer("Добренького. Справка по командам /help")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await  message.answer('"/ab" - Добавить себя в базу\n '
                          '"/db" - удалить себя из базы\n '
                          '"/ib" - посмотреть информацию в базе')


class Sb(StatesGroup):
    userID = State()
    nik = State()
    name = State()
    em = State()
    pa = State()
    po = State()
    dapa = State()


@dp.message(Command('ab'))
async def bID(mes: Message, state: FSMContext) -> None:
    await state.update_data(userID=mes.from_user.id)
    dat = await state.get_data()
    await state.set_state(Sb.nik)
    await mes.answer(text="Укажите ваш никнэйм.")
    logging.info("KUKU", [dat])


@dp.message(Sb.nik)
async def bNi(mes: Message, state: FSMContext) -> None:
    await state.update_data(nik=mes.text)
    dat = await state.get_data()
    logging.info("KUKU", [dat])
    await state.set_state(Sb.name)
    await mes.answer('Введите ваше имя.')


@dp.message(Sb.name)
async def bNa(mes: Message, state: FSMContext) -> None:
    await state.update_data(name=mes.text)
    dat = await state.get_data()
    logging.info("KUKU", [dat])
    await state.set_state(Sb.em)
    await mes.answer('Теперь email.')


@dp.message(Sb.em)
async def bEm(mes: Message, state: FSMContext) -> None:
    await state.update_data(em=mes.text)
    dat = await state.get_data()
    us = mes.from_user
    logging.info("KUKU", [dat, us])
    await mes.answer(text=f'ВЫ {dat["name"]} {dat["nik"]} почта:{dat["em"]}.\n Введите ваше послание')
    await state.set_state(Sb.po)


@dp.message(Sb.po)
async def bPo(mes: Message, state: FSMContext) -> None:
    await state.update_data(po=mes.text)
    await mes.answer(text='Осталось ввести пароль.')
    await state.set_state(Sb.pa)


@dp.message(Sb.pa)
async def bPa(mes: Message, state: FSMContext) -> None:
    await  state.update_data(pa=mes.text)
    dat = await state.get_data()
    await state.set_state(Sb.dapa)
    await mes.answer('Подтвердите пароль.')


@dp.message(Sb.dapa)
async def bPa(mes: Message, state: FSMContext) -> None:
    dat = await state.get_data()
    if mes.text == dat['pa']:

        try:
            @sync_to_async()
            def buza(dat, mes):
                user = User.objects.create_user(dat['nik'], dat['em'], dat['pa'])
                user.last_name = dat['name']
                user.save()

                ch = Chel(
                    tgid=mes.from_user.id,
                    tgna=mes.from_user.last_name,
                    tgni=mes.from_user.username,
                    id_id=user.id,
                    na=dat['nik'],
                    po=dat['po'],
                )
                ch.save()

            await buza(dat, mes)

        except Exception as err:
            await mes.answer(f'ошибка: {err}')
        else:
            await  mes.answer('Ваши данные сохранены')
    else:
        await mes.answer('Повторение не совподает.')


async def main_bot():
    try:
        await dp.start_polling(bot1)
    finally:
        await bot1.session.close()


@admin.action(description="Отправить сообщение")
def mes(modeladmin, request, queryset):
    for i in queryset.values_list("id", flat=True):
        ch = models.Chel.objects.get(id_id=i)
        m(ch.tgid,'Test')

class AdChel(admin.ModelAdmin):
    list_display = ('tgid', "tgni", "tgna", "na", "po",)
    search_fields = ('tgid', "tgni", "na", "po",)
    list_editable = ("na", "po",)
    actions = [mes]

admin.site.register(models.Chel, AdChel)


#if __name__ == "__main__":
    #asyncio.run(main_bot())

# t = Thread(target=lambda : asyncio.run(main_bot()))
# t.setDaemon(True)
# t.start()