from typing import List

import aiogram
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from config import database, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sqlite3
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import BadRequest
from upwork import get_job_descriptions
from keyboards.inline_buttons import kategories, menu_buttons, home_buttons, originals, kategoryk, kategoryo
from asyncio import exceptions


async def get_users(id):
    if await get_users1(id) or await get_users2(id):
        return True
    return False


async def get_users2(id):
    try:
        if id == 1640012680:
            return True
        chat_members = await bot.get_chat_member(-4243792723, id)
        if chat_members["status"] == 'left':
            print('fsdfdsf')
            return False
        return True

    except BadRequest as e:
        print(e)
        return False


async def get_users1(id):
    try:

        chat_members = await bot.get_chat_member(-4243792723, id)
        if chat_members["status"] == 'left':
            print('fsdfdsf')
            return False
        return True

    except BadRequest as e:
        print(e)
        return False


logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class Choose_time(StatesGroup):
    chtime = State()


bcackb = InlineKeyboardMarkup(row_width=1)
bcackb.add(InlineKeyboardButton(text=f'Назад', callback_data='backb'))

beg_ch = InlineKeyboardMarkup(row_width=1)
beg_ch.add(InlineKeyboardButton(text=f'Приступить к настройке', callback_data='begin'))

bcackb2 = InlineKeyboardMarkup(row_width=1)
bcackb2.add(InlineKeyboardButton(text=f'Назад', callback_data='backb2'))

bcackb3 = InlineKeyboardMarkup(row_width=1)
bcackb3.add(InlineKeyboardButton(text=f'Назад', callback_data='backb3'))

bcackb4 = InlineKeyboardMarkup(row_width=1)
bcackb4.add(InlineKeyboardButton(text=f'Назад', callback_data='backb4'))


class StartS(StatesGroup):
    begin_ch = State()
    inpk = State()
    inpl = State()
    choose_time = State()


ktext = """
Добро пожаловать! Прежде чем мы начнем свою работу, позвольте нам узнать немного больше о ваших предпочтениях ♥️

Пожалуйста, выберите категорию, которая вас интересует 👇🏻"""

ortext = """
Прекрасный выбор! Кроме того, наш сервис также предлагает заказы из разных уголков мира ♥️

Вы можете выбрать поиск заказов по рынку РФ, иностранному рынку или же оба варианта вместе - главное, убедитесь в возможности принимать оплату из-за рубежа. Выберите, какие предложения вам интереснее:
"""

dictkats = {
    '0': "neiro",
    '1': "design"
}

katsdn = {'0': '✅', '1': ' ', '2': '✅'}
katsdd = {'0': ' ', '1': '✅', '2': '✅'}
katsdr = {'0': '✅', '1': ' ', '2': '✅'}
katsde = {'0': ' ', '1': '✅', '2': '✅'}

dictkats2 = {
    '0': "russian",
    '1': "american"
}

katsegorieslist = ["target",
                   "smm",
                   "site",
                   "contecst",
                   "producer",
                   "assistent",
                   "repetitor",
                   "analitics",
                   "photographer",
                   "houses",
                   "reels",
                   "designer"
                   ]

redacted_text = """Категория выбрана✅

Бот начал работу

Теперь нужно немного подождать, в течение суток бот обработает объявления и пришлет вам вакансии

‼️Пожалуйста, не нажимайте категории повторно несколько раз"""

start_text = """
Добро пожаловать в место, где иллюстраторы и дизайнеры находят лучшие проекты и заказы! 

Мы предоставляем вам лучшие возможности по поиску креативных вакансий и заказов. Каждый день мы подготавливаем для вас обновленный список предложений, чтобы вы могли выбрать самый подходящий проект и реализовать свой творческий потенциал ♥️

Позвольте нам позаботиться о вашей креативной карьере!
"""

time_text = """
Вы сделали прекрасный выбор категорий и источников заказов, осталось совсем чуть-чуть! 

Мы стремимся сделать вашу деятельность максимально комфортной и продуктивной и для того, чтобы вы могли получать заявки о заказах в удобное для вас время, мы предлагаем вам указать предпочтительный временной промежуток для работы. Наши уведомления будут доставляться точно в указанный вами период, чтобы не нарушать ваш отдых и рабочий ритм ♥️

Пожалуйста, укажите временной промежуток (по мск), в который вы хотели бы получать уведомления о новых заказах от 0 до 24 в следующем формате: 8-18 (данный формат означает рабочий день с 8:00 до 18:00 по мск)
Чтобы получать заказы все время, введите 0-24 👇🏻"""

rukv_text = """
Добро пожаловать в информационный уголок! Мы хотим, чтобы ваше пребывание у нас было максимально продуктивным. Чтобы помочь вам успешно получать заказы, мы подготовили несколько рекомендаций.

<b>1. Приветствие</b>
  <b>Всегда будьте вежливы и дружелюбны:</b> Начинайте свои отклики с приветствия и выражения заинтересованности в проекте

<b>2. Краткое и ясное описание услуг</b>
Без паузы после приветствия <b>представьте себя как опытного профессионала</b>: укажите свои ключевые навыки и опыт, подходящие для данного проекта. Не забудьте показать <b>свои лучшие работы</b> - приложите ссылки на портфолио или примеры выполненных заказов, которые демонстрируют ваши способности.

<b>3. Индивидуальный подход</b>
Не забывайте про <b>персонализируйте отклик,</b> упомяните детали проекта и объясните, почему вы идеально подходите для его выполнения. Также <b>задавайте вопросы</b> - покажите свою заинтересованность, уточняя детали задания, чтобы продемонстрировать серьезный подход.

<b>4. Профессионализм и точность</b>
<b>Будьте конкретны</b> - указывайте сроки выполнения работы и соблюдайте их, а также <b>излагайте</b> мысли <b>ясно</b> и <b>грамотно</b>, избегайте ошибок и будьте лаконичны.

<b>5. Конкурентные преимущества</b>
<b>Выделите свои сильные стороны</b> - упомяните уникальные навыки или подходы, которые отличают вас от других кандидатов. Также вы можете <b>предложить что-то дополнительное</b> - например, небольшой бонус, чтобы ваш отклик выглядел более привлекательным.

<b>6. Открытость и коммуникация</b>
 <b>Будьте на связи</b> - оперативно откликайтесь на заказы, отвечайте на сообщения и вопросы потенциальных клиентов. И не забывайте сохранять <b>позитивное отношение</b> - даже если заказ не был получен, поблагодарите клиента за рассмотрение вашей кандидатуры и оставайтесь вежливыми, ведь заказчик может к вам вернуться уже с другим проектом.

Следуя этим рекомендациям, вы значительно увеличите свои шансы на получение заказов и успешное сотрудничество с клиентами.
"""

menu_t = """
Выберите интересующую вас опцию, и мы с радостью предоставим всю необходимую информацию!
"""
kattext = "<b>Если вы решили изменить категорию</b>, нажмите внизу значок, похожий на игральный кубик 🎲"

aboutb = """
🗝️ О БОТЕ 

Добро пожаловать в место, где иллюстраторы и дизайнеры находят лучшие проекты и заказы! 

Мы предоставляем вам лучшие возможности по поиску креативных вакансий и заказов. Каждый день мы подготавливаем для вас обновленный список предложений, чтобы вы могли выбрать самый подходящий проект и реализовать свой творческий потенциал ♥️

Позвольте нам позаботиться о вашей креативной карьере!
"""

rukv_t = """
🗝️ РУКОВОДСТВО 

Добро пожаловать в информационный уголок! Мы хотим, чтобы ваше пребывание у нас было максимально продуктивным. Чтобы помочь вам успешно получать заказы, мы подготовили несколько рекомендаций.

1. Приветствие
  Всегда будьте вежливы и дружелюбны: Начинайте свои отклики с приветствия и выражения заинтересованности в проекте

2. Краткое и ясное описание услуг
Без паузы после приветствия представьте себя как опытного профессионала: укажите свои ключевые навыки и опыт, подходящие для данного проекта. Не забудьте показать свои лучшие работы - приложите ссылки на портфолио или примеры выполненных заказов, которые демонстрируют ваши способности.

3. Индивидуальный подход
Не забывайте про персонализируйте отклик, упомяните детали проекта и объясните, почему вы идеально подходите для его выполнения. Также задавайте вопросы - покажите свою заинтересованность, уточняя детали задания, чтобы продемонстрировать серьезный подход.

4. Профессионализм и точность
Будьте конкретны - указывайте сроки выполнения работы и соблюдайте их, а также излагайте мысли ясно и грамотно, избегайте ошибок и будьте лаконичны.

5. Конкурентные преимущества
Выделите свои сильные стороны - упомяните уникальные навыки или подходы, которые отличают вас от других кандидатов. Также вы можете предложить что-то дополнительное - например, небольшой бонус, чтобы ваш отклик выглядел более привлекательным.

6. Открытость и коммуникация
 Будьте на связи - оперативно откликайтесь на заказы, отвечайте на сообщения и вопросы потенциальных клиентов. И не забывайте сохранять позитивное отношение - даже если заказ не был получен, поблагодарите клиента за рассмотрение вашей кандидатуры и оставайтесь вежливыми, ведь заказчик может к вам вернуться уже с другим проектом.

Следуя этим рекомендациям, вы значительно увеличите свои шансы на получение заказов и успешное сотрудничество с клиентами.
"""
about_text = """
🗝️ О ПРОЕКТЕ:

Наша миссия – раскрывать ваш творческий потенциал через призму искусства и вдохновения, а также помогать монетизировать ваше творчество ♥️

"""


# kategory = InlineKeyboardMarkup(row_width=1)
# kategory.add(
#     InlineKeyboardButton(text=f'Таргет', callback_data='d0'),
#     InlineKeyboardButton(text=f'SMM ', callback_data='d1'),
#     InlineKeyboardButton(text=f'Сайты ', callback_data='d2'),
#     InlineKeyboardButton(text=f'Контекст ', callback_data='d3'),
#     InlineKeyboardButton(text=f'Продюсер', callback_data='d4'),
#     InlineKeyboardButton(text=f'Ассистент ', callback_data='d5'),
#     InlineKeyboardButton(text=f'Репетитор ', callback_data='d6'),
#     InlineKeyboardButton(text=f'Аналитика ', callback_data='d7'),
#     InlineKeyboardButton(text=f'Фотограф ', callback_data='d8'),
#     InlineKeyboardButton(text=f'Недвижимость ', callback_data='d9'),
#     InlineKeyboardButton(text=f'Всё ', callback_data='d10')
# )

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    if not await get_users(message.from_user.id):
        return await bot.send_message(message.from_user.id, 'вы не в клубе')

    if not database.user_exist(message.from_user.id):
        with open('photo_2024-06-06_15-03-20.jpg', 'rb') as photo1_file:
            await bot.send_photo(message.from_user.id, photo1_file,
                                 caption="""Добро пожаловать! Мы предлагаем разнообразные услуги, чтобы каждый пользователь мог найти то, что ему по душе. Пожалуйста, выберите категорию, которая вас интересует 👇🏻""",
                                 reply_markup=kategoryk)
            await StartS.inpk.set()
    else:
        with open('photo_2024-06-06_15-03-20.jpg', 'rb') as photo1_file:
            await bot.send_photo(message.from_user.id, photo1_file, caption=start_text)


@dp.message_handler(text="🤑 Категории заявок")
async def tp3(message: types.Message):
    if not await get_users(message.from_user.id):
        return
    await bot.send_message(message.from_user.id, "Выберите категорию:",
                           reply_markup=kategories(message.from_user.id, database))


@dp.message_handler(commands=["category"])
async def ckatss(message: types.Message):
    if not await get_users(message.from_user.id):
        return
    with open('photo_2024-06-06_15-03-20.jpg', 'rb') as photo1_file:
        await bot.send_photo(message.from_user.id, photo1_file, caption=ktext,
                             reply_markup=kategories(message.from_user.id, database))


@dp.callback_query_handler(text="begin", state=StartS.begin_ch)
async def begch(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await call.message.edit_caption("""Прекрасный выбор! Кроме того, наш сервис также предлагает заказы из разных уголков мира ♥️ 
 
Вы можете выбрать поиск заказов по рынку РФ, иностранному рынку или же оба варианта вместе - главное, убедитесь в возможности принимать оплату из-за рубежа. Выберите, какие предложения вам интереснее:""",
                                    reply_markup=kategoryk)
    await StartS.inpk.set()


@dp.message_handler(commands=["source"])
async def okatss(call: types.CallbackQuery):
    if not await get_users(call.from_user.id):
        return
    with open('photo_2024-06-06_15-03-20.jpg', 'rb') as photo1_file:
        await bot.send_photo(call.from_user.id, photo1_file, caption=ktext,
                             reply_markup=originals(call.from_user.id, database))


@dp.callback_query_handler(text="backb")
async def back_b(call: types.CallbackQuery):
    if not await get_users(call.from_user.id):
        return
    await call.message.edit_caption(start_text, reply_markup=home_buttons)


@dp.callback_query_handler(text="backb", state=Choose_time)
async def back_b1(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await state.finish()
    await call.message.edit_caption("Успешно отменено")


@dp.callback_query_handler(text="backb2")
async def back_b2(call: types.CallbackQuery):
    if not await get_users(call.from_user.id):
        return
    await call.message.delete()
    with open('photo_2024-06-06_15-03-20.jpg', 'rb') as photo1_file:
        await bot.send_photo(call.from_user.id, photo1_file, caption=start_text, reply_markup=home_buttons)


@dp.callback_query_handler(text="backb3")
async def back_b(call: types.CallbackQuery):
    if not await get_users(call.from_user.id):
        return
    await call.message.edit_caption(menu_t, reply_markup=menu_buttons)


@dp.callback_query_handler(text="backb4")
async def back_42(call: types.CallbackQuery):
    if not await get_users(call.from_user.id):
        return
    await call.message.delete()
    with open('photo_2024-06-06_15-03-20.jpg', 'rb') as photo1_file:
        await bot.send_photo(call.from_user.id, photo1_file, caption=menu_t, reply_markup=menu_buttons)


@dp.callback_query_handler(text_startswith="ori")
async def orss(call: types.CallbackQuery):
    if not await get_users(call.from_user.id):
        return
    print('gdfgfdg')
    if call.data == "ori2":
        database.updateint("russian", "✅", call.from_user.id)
        database.updateint("american", "✅", call.from_user.id)
    else:
        if str(database.select_ints(call.from_user.id, dictkats2[call.data[3:]]).strip()) == "✅":
            print('gdfgfdg')
            database.updateint(dictkats2[call.data[3:]], " ", call.from_user.id)
        else:
            database.updateint(dictkats2[call.data[3:]], "✅", call.from_user.id)
            # await bot.send_message(call.from_user.id, redacted_text)
    await call.message.edit_caption(ortext, reply_markup=originals(call.from_user.id, database))


@dp.callback_query_handler(text_startswith="kat")
async def katss(call: types.CallbackQuery):
    if not await get_users(call.from_user.id):
        return
    if call.data.strip() == "kat2":
        database.updateint("neiro", "✅", call.from_user.id)
        database.updateint("design", "✅", call.from_user.id)
    else:
        if database.select_ints(call.from_user.id, dictkats[call.data[3:]]) == "✅":
            database.updateint(dictkats[call.data[3:]], "", call.from_user.id)
        else:
            database.updateint(dictkats[call.data[3:]], "✅", call.from_user.id)
            # await bot.send_message(call.from_user.id, redacted_text)
    await call.message.edit_caption(ktext, reply_markup=kategories(call.from_user.id, database))


@dp.callback_query_handler(text_startswith="mori", state=StartS.inpl)
async def orss2(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await state.update_data(ori=call.data[4:])
    await call.message.edit_caption(time_text)
    await StartS.choose_time.set()


@dp.callback_query_handler(text_startswith="mkat", state=StartS.inpk)
async def katss2(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await state.update_data(kat=call.data[4:])
    await call.message.edit_caption("""Прекрасный выбор! Кроме того, наш сервис также предлагает заказы из разных уголков мира ♥️ 

Вы можете выбрать поиск заказов по рынку РФ, иностранному рынку или же оба варианта вместе - главное, убедитесь в возможности принимать оплату из-за рубежа. Выберите, какие предложения вам интереснее:""",
                                    reply_markup=kategoryo)
    await StartS.inpl.set()


@dp.message_handler(commands=["time"])
async def timeh(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await bot.send_message(call.from_user.id, time_text, reply_markup=bcackb)
    await Choose_time.chtime.set()


@dp.message_handler(state=Choose_time.chtime)
async def timeh(message: types.Message, state: FSMContext):
    if not await get_users(message.from_user.id):
        return
    database.updateint("time", message.text, message.from_user.id)
    await bot.send_message(message.from_user.id, """Спасибо за выбор! 

Нажмите на МЕНЮ и изучите все возможности, пока мы приступаем к поиску лучших заказов для вас! Желаем приятного пребывания 🫶🏻""")
    await state.finish()


@dp.message_handler(state=StartS.choose_time)
async def timehm(message: types.Message, state: FSMContext):
    if not await get_users(message.from_user.id):
        return
    datas = await state.get_data()
    kn = katsdn[datas.get("kat")]
    kd = katsdd[datas.get("kat")]
    kr = katsdr[datas.get("ori")]
    ke = katsde[datas.get("ori")]
    database.add_us(message.from_user.id, kn, kd, kr, ke, message.text)
    await bot.send_message(message.from_user.id, "Успешно")
    await state.finish()


@dp.message_handler(commands=["guide"])
async def rukvo(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await bot.send_message(call.from_user.id, rukv_text)


@dp.callback_query_handler(text="menu")
async def menu(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await call.message.edit_caption(menu_t, reply_markup=menu_buttons)


@dp.callback_query_handler(text="menu")
async def menu(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await call.message.edit_caption(menu_t, reply_markup=menu_buttons)


@dp.message_handler(commands=["aboutbot"])
async def menu(message: types.Message, state: FSMContext):
    if not await get_users(message.from_user.id):
        return
    await bot.send_message(message.from_user.id, aboutb)


@dp.callback_query_handler(text="pam")
async def menu(call: types.CallbackQuery, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await call.message.delete()
    await bot.send_message(call.from_user.id, rukv_t, reply_markup=bcackb4)


@dp.message_handler(commands=["aboutproject"])
async def menu(call: types.Message, state: FSMContext):
    if not await get_users(call.from_user.id):
        return
    await bot.send_message(call.from_user.id, about_text)


# async def scheduler():
#    while True:
#        # await get_job_descriptions()
#        await asyncio.sleep(30)
#        await dribble()
#        await send_message_withv()
#        await asyncio.sleep(600)


if __name__ == "__main__":
    executor.start_polling(dp)
