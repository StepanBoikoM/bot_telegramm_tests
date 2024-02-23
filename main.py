import telebot
import requests
import sqlite3

from telebot import types
from config import  TOKEN
from keyboard import admins_keyboards,users_keyboards, number_keyboard
from db import check_table


bot = telebot.TeleBot(TOKEN)
check_table()

# Путь к файлу базы данных SQLite // ЗАМЕНИТЬ НА СВОЙ // (файл бд сейчас находиться  в той же папке, 
#что все файлы с кодом)

db_path = "sql.db"

def bot_start():
    try:
        print('Бот успешно запущен!')
    except:
        print('Произошла ошибка!')


@bot.message_handler(commands=['start'])
def handler_main(message):
    bot.send_message(message.chat.id, "🔎<b>Добро пожаловать!\nДавайте войдем в систему</b>🔎",
                     parse_mode='html',
                     reply_markup=number_keyboard())




def entrance(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, 'Оставьте ваш контактный номер для дальнейшего входа.', reply_markup=keyboard)

    bot.register_next_step_handler(message, contact)



@bot.message_handler(content_types=['contact'])
def contact(message):
        user_messages = message.contact.phone_number
        saved_message = user_messages
        if "+" not in saved_message:
               saved_message = "+" + saved_message


        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sql WHERE phone_number = ? OR work_number = ?",
                       (saved_message, saved_message))  # ищем результаты по номеру
        result = cursor.fetchone()
        if result:

            cursor.execute("UPDATE sql SET id_telegramm=? WHERE phone_number=? OR work_number = ?", (message.from_user.id,
                                                                                                     saved_message,
                                                                                                     saved_message))
            conn.commit()
            conn.close()
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            reg_button = types.KeyboardButton(text="/main")
            keyboard.add(reg_button)
            bot.send_message(message.chat.id, text=f'Вы успешно вошли в систему!', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, text=f'Произошла ошибка, вас нету в системе! Обратитесь к Администратору!')




def back_main(call):
   bot.send_message(call.chat.id, "<b>❗️Добро пожаловать❗️\nДавайте войдем в систему🔎</b>",
   parse_mode='html',
   reply_markup=number_keyboard())




@bot.message_handler(commands=['main'])
def handler_main(message):
    try:

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton('Войти как пользователь!', callback_data='user_entry'),
           types.InlineKeyboardButton('Войти как админ!', callback_data='admin_entry'))


        bot.send_message(message.chat.id, "<b>❗️Добро пожаловать❗️\nДавайте войдем в систему🔎</b>",
        parse_mode='html',
        reply_markup=markup)



    except TypeError:
        bot.send_message(message.chat.id, 'Произошла ошибка, вас нету в системе! Обратитесь к Администратору!')




def func_user(call):
    try:
      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()

      cursor.execute(f"SELECT status FROM sql WHERE id_telegramm = '{call.from_user.id}'")
      result = cursor.fetchone()[0]
      if result is not None and str(result) == 'admin':
          bot.send_message(call.from_user.id, 'Добро пожаловать в главное меню!\n\n🚨Вы вошли с ролью Администратора!🚨',
                               parse_mode='html',
                               reply_markup=admins_keyboards())

      else:
          bot.send_message(call.from_user.id, 'У вас нет прав для входа!')
    except TypeError:
      bot.send_message(call.from_user.id, 'У вас нет прав для входа!')





def func_admin(call):
    try:
      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()
  
      cursor.execute(f"SELECT status FROM sql WHERE id_telegramm = '{call.from_user.id}'")
      result = cursor.fetchone()[0]
      if result is not None and str(result) == 'user' or str(result) =='admin':
          bot.send_message(call.from_user.id, 'Добро пожаловать!\n\n👤Вы вошли с ролью Пользователя!👤',
                                  parse_mode='html',
                                  reply_markup=users_keyboards())
  
      else:
          bot.send_message(call.from_user.id, 'У вас нет прав для входа!')
    except TypeError:
      bot.send_message(call.from_user.id, 'У вас нет прав для входа!')


def smeta(message):
    url = 'https://imperial55.ru/webhook/'
    bot.send_message(message.chat.id, 'Перейдите по ссылке для перехода на сайт Сметы:\n ')
    bot.send_message(message.chat.id, url)


def add_admin(message):
    bot.send_message(message.chat.id,
                     '💡Введите имя Администратора:\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()

    if name.lower() == 'нет':
        handler_main(message)
    else:
        bot.register_next_step_handler(message, user_surname)
        bot.send_message(message.chat.id,
                         '💡Введите фамилию Администратора:\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')

def user_surname(message):
    global surname
    surname = message.text.strip()
    if surname.lower() == 'нет':
        handler_main()
    else:

        bot.send_message(message.chat.id,
                         '💡Введите отчество Администратора:\n❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, user_number)

def user_number(message):
    global pytrik
    pytrik = message.text.strip()
    if pytrik.lower() == 'нет':
        handler_main(message)
    else:

        bot.send_message(message.chat.id,
                         '💡Введите основной номер телефона Администратора:\nПример: +79456444850\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, work_number)

def work_number(message):
    global work_numero
    work_numero = message.text.strip()
    if work_numero.lower() == 'нет':
        handler_main(message)
    else:

        bot.send_message(message.chat.id,
                         '💡Введите рабочий номер телефона Администратора:\nПример: +79456444850\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, completion_admin)

def completion_admin(message):
    global numero
    numero = message.text.strip()
    if numero.lower() == 'нет':
        handler_main(message)
    else:

        user_id = message.chat.id
        bot.send_message(message.chat.id, '✔Добавлен Администратор❗❗❗', reply_markup=admins_keyboards())
        conn = sqlite3.connect('sql.db')
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO sql (name, surname,patronymic, work_number, phone_number, id_telegramm, status) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "admin")' % (
            name, surname, pytrik, work_numero, numero, user_id, ))
        conn.commit()
        cur.close()
        conn.close()

def ID_user(message):
    bot.send_message(message.chat.id,
                     '💡Введите ID Пользователя:\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
    bot.register_next_step_handler(message, adduss)




def adduss(message):
    global userID
    userID = message.text.strip()
    if userID.lower() == 'нет':
        handler_main(message)
    else:
        bot.send_message(message.chat.id,
                         '💡Введите имя Пользователя:\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, aser_name)


def aser_name(message):
    global nameUser
    nameUser = message.text.strip()
    if nameUser.lower() == 'нет':
        handler_main(message)
    else:
        bot.send_message(message.chat.id,
                         '💡Введите фамилию Пользователя:\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, aser_surname)


def aser_surname(message):
    global surnameUser
    surnameUser = message.text.strip()
    if surnameUser.lower() == 'нет':
        handler_main(message)
    else:
        bot.send_message(message.chat.id,
                         '💡Введите отчество Пользователя:\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, aser_pytrik)


def aser_pytrik(message):
    global pytrikUser
    pytrikUser = message.text.strip()
    if pytrikUser.lower() == 'нет':
        handler_main(message)
    else:
        bot.send_message(message.chat.id,
                         '💡Введите рабочий номер телефона Пользователя:\nПример: +79456444850\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, work_numerUser)


def work_numerUser(message):
    global work_numeroUser
    work_numeroUser = message.text.strip()
    if work_numeroUser.lower() == 'нет':
        handler_main(message)
    else:
        bot.send_message(message.chat.id,
                         '💡Введите рабочий номер телефона Пользователя:\nПример: +79456444850\n ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
        bot.register_next_step_handler(message, phone_numerUser)


def phone_numerUser(message):
    try:
        global numeroUser
        numeroUser = message.text.strip()

        if numeroUser.lower() == 'нет':
            handler_main(message)

        else:
            status = 'user'
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO sql (ID, name, surname, patronymic, work_number, phone_number, status) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (userID, nameUser, surnameUser, pytrikUser, work_numeroUser, numeroUser, status))
            conn.commit()
            cur.close()
            conn.close()

            bot.send_message(message.chat.id, '✔️Добавлен Пользователь❗️❗️❗️')
            bot.send_message(message.chat.id, text='🔎Выберите опцию🔎', parse_mode='html', reply_markup=admins_keyboards())

    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, '❗️❗️❗️ОШИБКА, ТАКОЕ ЗНАЧЕНИЕ УЖЕ СУЩЕСТВУЕТ❗️❗️❗️')



def view_admin(message):

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM sql WHERE status="admin"')
    users = cur.fetchall()

    for el in users:
        bot.send_message(message.chat.id, text=f'🆔:{el[0]}\n⬇️⬇️⬇️⬇️⚖️⚖️⚖️\n 🔑Имя:{el[1]}\n 🔑Фамилия:{el[2]}\n 🔑Отчество:{el[3]}\n 💬📠Рабочий номер:{el[4]}\n 📞📱Номер:{el[5]}\n\n ➖➖➖💾➖➖➖\n\n')

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, text='🔎Выберите опцию🔎', parse_mode='html', reply_markup=admins_keyboards())

def viewusers(message):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM sql WHERE status="user"')
    users = cur.fetchall()
    for el in users:
        bot.send_message(message.chat.id,
                         text=f'🆔:{el[0]}\n⬇️⬇️⬇️⬇️⚖️⚖️⚖️\n 🔑Имя:{el[1]}\n 🔑Фамилия:{el[2]}\n 🔑Отчество:{el[3]}\n 💬📠Рабочий номер:{el[4]}\n 📞📱Номер:{el[5]}\n\n ➖➖➖💾➖➖➖\n\n')


    cur.close()
    conn.close()
    bot.send_message(message.chat.id, text='🔎Выберите опцию🔎', parse_mode='html', reply_markup=admins_keyboards())




def remove_ad(message):
    view_admin(message)
    bot.send_message(message.chat.id,
                     'Введите id админа которого хотите удалить: ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
    bot.register_next_step_handler(message, rem_adi)

def remove_pl(message):
    viewusers(message)
    bot.send_message(message.chat.id,
                     'Введите id пользователя которого хотите удалить: ❗❗❗(Если хотите отменить действие, напишите "нет" в данном сообщении)❗❗❗')
    bot.register_next_step_handler(message, remove_pol)

def rem_adi(message):
    global addminID
    addminID = message.text.strip()
    if addminID.lower() == 'нет':
        handler_main(message)
    else:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM sql WHERE ID=?", (addminID,))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, '❗❗❗админ удален❗❗❗', replay_markup=back_main())




def remove_pol(message):
    global polzavID
    polzavID = message.text.strip()
    if polzavID.lower() == 'нет':
        handler_main(message)
    else:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM sql WHERE ID=?", (polzavID,))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, '❗❗❗Пользователь удален❗❗❗', reply_markup=admins_keyboards())



def get(message):
    bot.send_message(message.chat.id, 'Введите ID сделки: ')
    bot.register_next_step_handler(message, getIDD)


def getIDD(message):
    conn = sqlite3.connect('sql.db')
    cur = conn.cursor()
    id_tg = message.from_user.id

    #Запрос к базе данных и возвращает ID пользователя
    #с наивысшим статусом (администратором), если есть
    #несколько записей с одинаковым номером телефона:
    sql_query = f"""
    SELECT ID 
    FROM sql 
    WHERE id_telegramm = '{id_tg}' 
    ORDER BY CASE WHEN status = 'admin' THEN 1 ELSE 2 END
    LIMIT 1;
    """

    # Выполнение запроса
    cur.execute(sql_query)
    result = cur.fetchone()
    conn.close()
    user_id = result[0]
    print(user_id)

    if result:
        getID = message.text.strip()
        getID.encode('utf-8')
        
        
        url = f"https://imperial55.ru/webhook/dealget.php?ID={getID}&mID={user_id}&close=N"
        print(url)
        
        response = requests.get(url)
        bot.send_message(message.chat.id, 'Закрытая сделка:')
        
        for key in response.text.splitlines():
            a = len(key)  # разделить ответ по строкам
            if a > 59:
                bot.send_message(message.chat.id, key)
            else:
                bot.send_message(message.chat.id, 'Пустая сделка')
        bot.send_message(message.chat.id, f'Главное меню!', reply_markup=users_keyboards())
        if response.status_code == 200:
            return response.text
        else:
            return 'Ошибка получения данных'
    else:
        print("Пользователь не найден! Произошла ошибка!")



def get_close(message):
    bot.send_message(message.chat.id, 'Введите ID сделки: ')
    bot.register_next_step_handler(message, close_get)

def close_get(message):
    conn = sqlite3.connect('sql.db')
    cur = conn.cursor()
    id_tg = message.from_user.id

    #Запрос к базе данных и возвращает ID пользователя
    #с наивысшим статусом (администратором), если есть
    #несколько записей с одинаковым номером телефона:
    sql_query = f"""
    SELECT ID 
    FROM sql 
    WHERE id_telegramm = '{id_tg}' 
    ORDER BY CASE WHEN status = 'admin' THEN 1 ELSE 2 END
    LIMIT 1;
    """

    # Выполнение запроса
    cur.execute(sql_query)
    result = cur.fetchone()
    conn.close()
    user_id = result[0]
    print(user_id)

    if result:
        getID = message.text.strip()
        getID.encode('utf-8')
        
        
        url = f"https://imperial55.ru/webhook/dealget.php?ID={getID}&mID={user_id}&close=Y"
        print(url)
        
        response = requests.get(url)
        bot.send_message(message.chat.id, 'Закрытая сделка:')
        
        for key in response.text.splitlines():
            a = len(key)  # разделить ответ по строкам
            if a > 59:
                bot.send_message(message.chat.id, key)
            else:
                bot.send_message(message.chat.id, 'Пустая сделка')
        bot.send_message(message.chat.id, f'Главное меню!', reply_markup=users_keyboards())
        if response.status_code == 200:
            return response.text
        else:
            return 'Ошибка получения данных'
    else:
        print("Пользователь не найден! Произошла ошибка!")


def all_deal(call):
    try:
        conn = sqlite3.connect('sql.db')
        cur = conn.cursor()
        id_tg = call.from_user.id

        #Запрос к базе данных и возвращает ID пользователя
        #с наивысшим статусом (администратором), если есть
        #несколько записей с одинаковым номером телефона:
        sql_query = f"""
        SELECT ID 
        FROM sql 
        WHERE id_telegramm = '{id_tg}' 
        ORDER BY CASE WHEN status = 'admin' THEN 1 ELSE 2 END
        LIMIT 1;
        """

        # Выполнение запроса
        cur.execute(sql_query)
        result = cur.fetchone()
        conn.close()

        if result:
            user_id = result[0]
            print(f"ID пользователя с наивысшим статусом (администратором): {user_id}")
            url = f"https://imperial55.ru/webhook/dealget.php?mID={user_id}&close=N"
            print(url)

            response = requests.get(url)
            response_text = response.content.decode('utf-8')
            bot.send_message(call.from_user.id, 'Все  открытые сделки:')
            if response_text:
                bot.send_message(call.from_user.id, response_text)
                bot.send_message(call.from_user.id, 'Главное меню!', reply_markup=users_keyboards())

            else:
                bot.send_message(call.from_user.id, 'Открытые сделки отсутствуют!')
                bot.send_message(call.from_user.id, 'Главное меню!', reply_markup=users_keyboards())


        else:
            print("Пользователь с таким номером телефона не найден")
    except TypeError as e:
       print(f'ошибка {e}')




def all_close_deal(call):
    try:
        conn = sqlite3.connect('sql.db')
        cur = conn.cursor()
        id_tg = call.from_user.id

        #Запрос к базе данных и возвращает ID пользователя
        #с наивысшим статусом (администратором), если есть
        #несколько записей с одинаковым номером телефона:
        sql_query = f"""
        SELECT ID 
        FROM sql 
        WHERE id_telegramm = '{id_tg}' 
        ORDER BY CASE WHEN status = 'admin' THEN 1 ELSE 2 END
        LIMIT 1;
        """


        cur.execute(sql_query)
        result = cur.fetchone()
        conn.close()

        if result:
            user_id = result[0]
            print(f"ID пользователя с наивысшим статусом (администратором): {user_id}")
            url = f"https://imperial55.ru/webhook/dealget.php?mID={user_id}&close=Y"
            print(url)

            response = requests.get(url)
            response_text = response.content.decode('utf-8')
            bot.send_message(call.from_user.id, 'Все  Закрытые сделки:')
            if response_text:
                bot.send_message(call.from_user.id, response_text)
                bot.send_message(call.from_user.id, 'Главное меню!', reply_markup=users_keyboards())

            else:
                bot.send_message(call.from_user.id, 'Закрытые сделки отсутствуют!')
                bot.send_message(call.from_user.id, 'Главное меню!', reply_markup=users_keyboards())


        else:
            print("Пользователь с таким номером телефона не найден")



    except TypeError as e:
        print(f'ошибка {e}')





@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'add_admin':
           add_admin(call.message)
    elif call.data == 'add_user':
            ID_user(call.message)
    elif call.data == 'view_users':
           viewusers(call.message)
    elif call.data == 'view_admin':
           view_admin(call.message)
    elif call.data == 'remove_admin':
            remove_ad(call.message)
    elif call.data == 'remove_user':
            remove_pl(call.message)

    elif call.data == 'go_contact':
            entrance(call.message)
    elif call.data == 'ad_back':
            handler_main(call.message)
    elif call.data == 'back_menu':
           back_main(call.message)
    elif call.data == 'vie_del':
           get(call.message)
    elif call.data == 'smeta':
           smeta(call.message)
    elif call.data == 'all_vie_del':
        all_deal(call)
    elif call.data == 'close_vie_del':
           get_close(call.message)
    elif call.data == 'all_close_via_del':
           all_close_deal(call)
    elif call.data == 'admin_entry':
        func_user(call)
    elif call.data == 'user_entry':
        func_admin(call)


if __name__ == '__main__':
  bot.infinity_polling(bot_start())

