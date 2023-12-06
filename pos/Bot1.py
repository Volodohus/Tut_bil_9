import asyncio
import logging
from django.contrib.auth.models import User
from .models import Chel
from aiogram.client import bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram import F
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Filter
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from .tokid import toki,idVo
# ДЗ: сделать бота, который будет запрашивать данные пользователя и сохранять их в стейт.
# Со звездочкой: так же сохранять и в базу данных.

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot1 = bot.Bot(token= toki)
dp = Dispatcher()

@dp.startup()
async def start():
    await bot1.send_message(idVo,'Поехали!')



@dp.message(Command( "start"))
async def cmd_start(message: types.Message):
    await  message.answer("Добренького. Справка по командам /help")

@dp.message(Command( "help"))
async def cmd_help(message: types.Message):
    await  message.answer('"/ab" - Добавить себя в базу\n '
                          '"/db" - удалить себя из базы\n '
                          '"/ib" - посмотреть информацию в базе')


class Sb(StatesGroup):
    userID  = State()
    nik     = State()
    name    = State()
    em      = State()
    pa      = State()
    dapa    = State()

@dp.message(Command('ab'))
async def bID(mes: Message, state: FSMContext) -> None:
    await state.update_data(userID = mes.from_user.id)
    dat = await state.get_data()
    await state.set_state(Sb.nik)
    await mes.answer(text="Укажите ваш никнэйм.")
    logging.info("KUKU",  [dat])

@dp.message(Sb.nik)
async  def bNi(mes: Message, state: FSMContext) -> None:
    await state.update_data(nik=mes.text)
    dat = await state.get_data()
    logging.info("KUKU", [dat])
    await state.set_state(Sb.name)
    await mes.answer('Введите ваше имя.')

@dp.message(Sb.name)
async  def bNa(mes: Message, state: FSMContext) -> None:
    await state.update_data(name=mes.text)
    dat = await state.get_data()
    logging.info("KUKU", [dat])
    await state.set_state(Sb.em)
    await mes.answer('Теперь email.')

@dp.message(Sb.em)
async  def bEm(mes: Message, state: FSMContext) -> None:
    await state.update_data(em=mes.text)
    dat = await state.get_data()
    us = mes.from_user
    logging.info("KUKU", [dat,us])
    await mes.answer(text =f'ВЫ {dat["name"]} {dat["nik"]} почта:{dat["em"]}.\nТеперь нужно ввести пароль.')
    await state.set_state(Sb.pa)

@dp.message(Sb.pa)
async def bPa(mes: Message, state: FSMContext) -> None:
    await  state.update_data(pa=mes.text)
    dat = await state.get_data()
    logging.info("KUKU", [dat,])
    await state.set_state(Sb.dapa)
    await mes.answer('Подтвердите пароль.')

@dp.message(Sb.dapa)
async def bPa(mes: Message, state: FSMContext) -> None:
    dat = await state.get_data()
    if mes.text == dat['pa']:
        try:
            user = User.objects.create_user(dat['nik'],dat['em'],dat['pa'])
            user.last_name = dat['name']
            user.save()

            ch = Chel(tgid=mes.from_user.id, tgna=mes.from_user.last_name, tgni=mes.from_user.username,id_id=user.id)
            ch.save()
        except:
            await mes.answer('ошибка')
        finally:
            await  mes.answer('Ваши данные сохранены')
    else:
        await mes.answer('Повторение не совподает.')


async def main():
    try:

        await dp.start_polling(bot1)

    finally:
        bot1.session.close() # эта штука позволяет читать пропущенные.
        #Т.е. если сессию не закрывать, то при повторном запуске ты не получишь пропущенные.
        #Сервер телеграма, будет считать что бот все прочетал. Так устроен аиограм, наверно.
        #зависит от того каким из двух способов аиограм(незнаю) работает с сервером телеграмма.

#if __name__ == "__main__":
#    asyncio.run(main(),start())