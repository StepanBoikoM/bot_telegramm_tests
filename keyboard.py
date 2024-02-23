#ЗДЕСЬ НАХОДИТЬСЯ КЛАВИАТУРА

from telebot import types


def users_keyboards():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('🎫Просмотр открытой сделки🎫', callback_data='vie_del'),
               types.InlineKeyboardButton('🎫Все  открытые сделки🎫', callback_data='all_vie_del'),
               types.InlineKeyboardButton('🎫Просмотр закрытой сделки🎫 ', callback_data='close_vie_del'),
               types.InlineKeyboardButton('🎫СМЕТА🎫', callback_data='smeta'),
               types.InlineKeyboardButton('🎫Все закрытые сделки🎫', callback_data='all_close_via_del'),
               types.InlineKeyboardButton('❗❗❗Выйти в главное меню❗❗❗', callback_data='back_menu'), )
    return markup


def admins_keyboards():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('👮Добавить Админа✍', callback_data='add_admin'),
               types.InlineKeyboardButton('👔Добавить Пользователя✍', callback_data='add_user'),
               types.InlineKeyboardButton('👮Удалить Админа💥', callback_data='remove_admin'),
               types.InlineKeyboardButton('👔Удалить Пользователя либо админа💥', callback_data='remove_user'),
               types.InlineKeyboardButton('🎫СМЕТА🎫', callback_data='smeta'),
               types.InlineKeyboardButton('👔Пользователи👔', callback_data='view_users'),
               types.InlineKeyboardButton('👮Администрация👮', callback_data='view_admin'),
               types.InlineKeyboardButton('❗❗❗Выйти в главное меню❗❗❗', callback_data='back_menu'), )
    return markup


def number_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Поделиться номером телефона', callback_data='go_contact'), )
    return markup


def contact_keyboards():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(reg_button)
    return keyboard

