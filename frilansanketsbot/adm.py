import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

from database import Database
from funcs import read_file_s, write_file, read_file

logging.basicConfig(level=logging.INFO)
pagination_cb = CallbackData('pagination', 'category', 'page', 'action')

# Инициализация бота и диспетчера
bot_token = '7122868873:AAH2LFdtgKK7yIy0wFBJaUcbeHq3ypW1IWc'
bot = Bot(token=bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

database = Database("database.db")

admin_buttons = InlineKeyboardMarkup(row_width=2)
admin_buttons.add(InlineKeyboardButton(text='Добавить', callback_data='add_admin'),
                  InlineKeyboardButton(text='Удалить', callback_data='del_admin'))

ban_words_b = InlineKeyboardMarkup(row_width=2)
ban_words_b.add(InlineKeyboardButton(text='Добавить', callback_data='ban_add'),
                InlineKeyboardButton(text='Удалить', callback_data='ban_del'))


class Admins(StatesGroup):
    admin_id = State()
    admin_username = State()


class DelAdmins(StatesGroup):
    del_admins = State()


def format_admins():
    c = ""
    admins_id = read_file_s("admin_id.txt")
    admins_username = read_file_s("admin_username.txt")

    for i in range(len(admins_id)):
        c = c + f"ID: <b>{admins_id[i]}</b> Username: <b>@{admins_username[i]}</b>;\n"
    return c


class AddBf(StatesGroup):
    add_bf = State()
    add_file_kw = State()
    del_bf = State()


# Состояния
class KeywordStates(StatesGroup):
    add_keyword = State()
    del_keyword = State()
    select_category = State()


class ExchangeStates(StatesGroup):
    manage_exchange = State()


backbutton1 = InlineKeyboardMarkup(row_width=2)
backbutton1.add(InlineKeyboardButton(text='Отменить', callback_data='wbackb1'))

backbutton2 = InlineKeyboardMarkup(row_width=2)
backbutton2.add(InlineKeyboardButton(text='Отменить', callback_data='wbackb2'))

backbutton8 = InlineKeyboardMarkup(row_width=2)
backbutton8.add(InlineKeyboardButton(text='Отменить', callback_data='wbackb8'))


# Основное меню администратора
def admin_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Настройка ключевых слов')).add(
        KeyboardButton('Настройка бирж')
    ).add("Администраторы⭐️").add("Бан-Фразы🚫")


# Инлайн-кнопки для настройки ключевых слов
def keyword_menu():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('дизайнru', callback_data='keywords_designru'),
        InlineKeyboardButton('airu', callback_data='keywords_airu'),
        InlineKeyboardButton('дизайнen', callback_data='keywords_designen'),
        InlineKeyboardButton('aien', callback_data='keywords_aien')
    )


# Инлайн-кнопки для добавления и удаления ключевых слов
def keyword_actions_menu(category):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('Добавить ключевое слово', callback_data=f'ak_{category}'),
        InlineKeyboardButton('Удалить ключевое слово', callback_data=f'dk_{category}')
    )


# Инлайн-кнопки для настройки бирж
def exchange_menu():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('Fiverr', callback_data='exchange_fiverr'),
        InlineKeyboardButton('Upwork', callback_data='exchange_upwork'),
        InlineKeyboardButton('Behance', callback_data='exchange_behance'),
        InlineKeyboardButton('Dribble', callback_data='exchange_dribble')
    )


# Стартовый хендлер
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Вы в админ-меню", reply_markup=admin_menu())


# Настройка ключевых слов
@dp.message_handler(lambda message: message.text == 'Настройка ключевых слов')
async def setup_keywords(message: types.Message):
    await message.answer("Выберите категорию для настройки ключевых слов:", reply_markup=keyword_menu())


@dp.message_handler(text='Администраторы⭐️')
async def admin(message: types.Message):
    if str(message.from_user.id) not in read_file_s("admin_id.txt"):
        return
    await bot.send_message(message.from_user.id, f'Админы :\n\n{format_admins()}', reply_markup=admin_buttons)


@dp.callback_query_handler(text='add_admin')
async def add_id_admin(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in read_file_s("admin_id.txt"):
        return
    await call.message.edit_text('Впишите id админа, которого хотите добавить', reply_markup=backbutton1)
    await Admins.admin_id.set()


@dp.message_handler(state=Admins.admin_id)
async def add_admin_id(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in read_file_s("admin_id.txt"):
        return
    await state.update_data(id=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.from_user.id, 'Теперь введите его username', reply_markup=backbutton1)
    await Admins.admin_username.set()


@dp.message_handler(state=Admins.admin_username)
async def add_admin_username(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in read_file_s("admin_id.txt"):
        return
    f = await state.get_data()

    admin_ids = read_file_s("admin_id.txt")
    admin_usernames = read_file_s("admin_username.txt")

    admin_ids.append(f.get('id'))
    admin_usernames.append(message.text)
    write_file("admin_id.txt", " ".join(admin_ids))
    write_file("admin_username.txt", " ".join(admin_usernames))

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.from_user.id, 'Успешно!\n', reply_markup=admin_menu())
    await state.finish()


@dp.callback_query_handler(text='del_admin')
async def del_admin_id(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in read_file_s("admin_id.txt"):
        return
    await call.message.edit_text('Впишите username админа, которого хотите удалить', reply_markup=backbutton2)
    await DelAdmins.del_admins.set()


@dp.message_handler(state=DelAdmins.del_admins)
async def get_admin_del_id(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in read_file_s("admin_id.txt"):
        return
    admin_ids = read_file_s("admin_id.txt")
    admin_usernames = read_file_s("admin_username.txt")
    index = admin_usernames.index(message.text)
    admin_ids.pop(index)
    admin_usernames.pop(index)
    write_file("admin_id.txt", " ".join(admin_ids))
    write_file("admin_username.txt", " ".join(admin_usernames))

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.from_user.id, 'Успешно!\n', reply_markup=admin_menu())
    await state.finish()


@dp.callback_query_handler(text='wbackb1', state=Admins)
async def warning1(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in read_file_s("admin_id.txt"):
        return
    print('works')
    await call.message.edit_text(f'Админы :\n\n{format_admins()}', reply_markup=admin_buttons)
    await state.finish()


@dp.message_handler(text='Бан-Фразы🚫')
async def ban_phr(message: types.Message):
    if str(message.from_user.id) not in read_file_s("admin_id.txt"):
        return
    t = "; \n".join(read_file("banf.txt").split(' $ '))
    await bot.send_message(message.from_user.id, f'Бан-слова: <i>\n{t}</i>',
                           reply_markup=ban_words_b)


@dp.callback_query_handler(text='ban_add')
async def add_ban_w(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in read_file_s("admin_id.txt"):
        return
    await call.message.edit_text(
        'Скиньте фразу/слово, которое хотите добавить, чтобы при наличии этой фразы в сообщение оно не '
        'пропускалось', reply_markup=backbutton8)
    await AddBf.add_bf.set()


@dp.message_handler(state=AddBf.add_bf)
async def get_bf(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in read_file_s("admin_id.txt"):
        return
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    write_file("banf.txt", f"{read_file('banf.txt')} $ {message.text}")
    t = "; \n\t".join(read_file("banf.txt").split(' $ '))

    await bot.send_message(message.from_user.id, f'Успешно!\nБан-слова: \n\t{t}', reply_markup=ban_words_b)
    await state.finish()


@dp.callback_query_handler(text='ban_del')
async def del_bf_id(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in read_file_s("admin_id.txt"):
        return
    await call.message.edit_text('Скиньте слово/фразу, которое хотите удалить', reply_markup=backbutton8)
    await AddBf.del_bf.set()


@dp.message_handler(state=AddBf.del_bf)
async def get_bf_del_id(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in read_file_s("admin_id.txt"):
        return
    wow = read_file("banf.txt").split(" $ ")
    wow.remove(message.text)
    write_file("banf.txt", " $ ".join(wow))
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    t = "; \n\t".join(read_file("banf.txt").split(' $ '))

    await bot.send_message(message.from_user.id, f'Успешно!\n\nБан-слова: <i>\n\t{t}</i>', reply_markup=ban_words_b)
    await state.finish()


@dp.callback_query_handler(text='wbackb8', state=AddBf)
async def warning8(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in read_file_s("admin_id.txt"):
        return
    print('works')
    t = "; \n".join(read_file("banf.txt").split(' $ '))

    await call.message.edit_text(f'Бан-слова: {t}', reply_markup=ban_words_b)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('keywords_'))
async def manage_keywords(call: types.CallbackQuery):
    category = call.data.split('_')[1]
    print(category)
    keywords = database.get_keywords(category)
    await call.message.edit_text(f"Ключевые слова для {category}:\n{', '.join(keywords)}",
                                 reply_markup=keyword_actions_menu(category))


# Добавление ключевого слова
@dp.callback_query_handler(lambda c: c.data.startswith('ak_'))
async def start_adding_keyword(call: types.CallbackQuery):
    category = call.data.split('_')[1]
    await call.message.answer(f"Введите новое ключевое слово для категории {category}:")
    await KeywordStates.add_keyword.set()
    await dp.current_state(user=call.from_user.id).update_data(category=category)


@dp.message_handler(state=KeywordStates.add_keyword)
async def add_keyword(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category = data['category']
    keyword = message.text
    database.add_keyword(category, keyword)
    await message.answer(f"Ключевое слово '{keyword}' добавлено в категорию {category}.", reply_markup=admin_menu())
    await state.finish()


def create_paginated_keyboard(category, keywords, page=0, items_per_page=5):
    max_page = (len(keywords) - 1) // items_per_page
    keyboard = InlineKeyboardMarkup(row_width=1)
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    for keyword in keywords[start_index:end_index]:
        keyboard.add(InlineKeyboardButton(keyword, callback_data=f'd_{category}_{keyword}'))

    # Добавление кнопок навигации
    if page > 0:

        if page < max_page:
            keyboard.row(InlineKeyboardButton("⏪", callback_data=pagination_cb.new(category=category, page=page - 1,
                                                                                   action='prev')),
                         InlineKeyboardButton("⏩",
                                              callback_data=pagination_cb.new(category=category, page=page + 1,
                                                                              action='next')))
        else:
            keyboard.add(
                InlineKeyboardButton("⏪",
                                     callback_data=pagination_cb.new(category=category, page=page - 1, action='prev')))


    else:
        keyboard.add(
            InlineKeyboardButton("⏩", callback_data=pagination_cb.new(category=category, page=page + 1, action='next')))

    return keyboard


# Обработчик для начала удаления ключевых слов
@dp.callback_query_handler(lambda c: c.data.startswith('dk_'))
async def start_deleting_keyword(call: types.CallbackQuery):
    category = call.data.split('_')[1]
    keywords = database.get_keywords(category)
    if keywords:
        keyboard = create_paginated_keyboard(category, keywords)
        await call.message.answer(f"Выберите ключевое слово для удаления из категории {category}:",
                                  reply_markup=keyboard)
    else:
        await call.message.answer(f"В категории {category} нет ключевых слов для удаления.",
                                  reply_markup=keyword_menu())


# Обработчик для пагинации
@dp.callback_query_handler(pagination_cb.filter(action=['prev', 'next']))
async def paginate_keywords(call: types.CallbackQuery, callback_data: dict):
    category = callback_data['category']
    page = int(callback_data['page'])
    keywords = database.get_keywords(category)
    keyboard = create_paginated_keyboard(category, keywords, page)
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('d_'))
async def delete_keyword(call: types.CallbackQuery):
    _, category, keyword = call.data.split('_', 2)
    database.delete_keyword(keyword)
    await call.message.answer(f"Ключевое слово '{keyword}' удалено из категории {category}.", reply_markup=admin_menu())


# Настройка бирж
@dp.message_handler(lambda message: message.text == 'Настройка бирж')
async def setup_exchanges(message: types.Message):
    await message.answer("Выберите биржу для настройки:", reply_markup=exchange_menu())


@dp.callback_query_handler(lambda c: c.data.startswith('exchange_'))
async def manage_exchanges(call: types.CallbackQuery):
    exchange = call.data.split('_')[1]
    # Пример получения и изменения статуса биржи (реализуйте логику в базе данных)
    status = database.get_exchange_status(exchange)
    new_status = '✔' if status == '' else ''
    database.set_exchange_status(exchange, new_status)
    await call.message.edit_text(f"Биржа {exchange} настроена на {new_status}", reply_markup=exchange_menu())


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
