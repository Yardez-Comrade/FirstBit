import time
import telebot
from telebot import types
from threading import Thread
import datetime
import schedule
import requests
from isoweek import Week
import asyncio
from Send_FirstBit import *

url = 'https://api.telegram.org/bot'
bot_token = '6281850578:AAEMV7oyiUkObYsyh8Qi672FZniXEMZX0mE'
bot = telebot.TeleBot(bot_token)
now_date = ''
employee_status = ''
flag_begin_time = False
week_start_send_others_days = 0

print('🥳 START PROGRAMM 🥳')


def start_markup_choose():  # Выбор должности
    keyboard = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton(text='👨‍💻 Сотрудник', callback_data='employee')
    admin = types.InlineKeyboardButton(text='👨‍💻 Администратор', callback_data='admin')
    keyboard.add(student)
    keyboard.add(admin)
    return keyboard

def markup_choose_employee():
    keyboard = types.InlineKeyboardMarkup()
    student = types.InlineKeyboardButton(text='👩‍💼 Офисный', callback_data='office')
    admin = types.InlineKeyboardButton(text='🧑‍💻 Удалённый', callback_data='remote')
    keyboard.add(student)
    keyboard.add(admin)
    return keyboard

def work_file_main(itog):
    with open('main_file.txt', 'r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line.split()
            try:
                if itog == line[0]:
                    if line[0] == "passwords":
                        line.pop(0)
                        return line
            except Exception:
                pass

def manegers_names():
    keyboard = types.InlineKeyboardMarkup()
    manager1 = types.InlineKeyboardButton(text='Марина', callback_data='manager1')
    manager2 = types.InlineKeyboardButton(text='Анна', callback_data='manager2')
    manager3 = types.InlineKeyboardButton(text='Лиза', callback_data='manager3')
    manager4 = types.InlineKeyboardButton(text='Виктоия', callback_data='manager4')
    manager5 = types.InlineKeyboardButton(text='Дарья', callback_data='manager5')
    manager6 = types.InlineKeyboardButton(text='Юлия', callback_data='manager6')
    manager7 = types.InlineKeyboardButton(text='Елена', callback_data='manager7')
    manager8 = types.InlineKeyboardButton(text='Наталья', callback_data='manager8')
    keyboard.add(manager1)
    keyboard.add(manager2)
    keyboard.add(manager3)
    keyboard.add(manager4)
    keyboard.add(manager5)
    keyboard.add(manager6)
    keyboard.add(manager7)
    keyboard.add(manager8)
    return keyboard

def admin_panel():  # Админская панель
    keyboard = types.InlineKeyboardMarkup()
    send_all = types.InlineKeyboardButton(text='📬 Рассылка', callback_data='send_panel')
    users = types.InlineKeyboardButton(text='👥 Вывести ваших сотрудников', callback_data='print_users')
    keyboard.add(send_all)
    keyboard.add(users)
    return keyboard

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    a = types.KeyboardButton(text='☎️ Контакт моего МПП')
    b = types.KeyboardButton(text='💠 Ресепшн')
    c = types.KeyboardButton(text='📑 Справки')
    d = types.KeyboardButton(text='✈️ Отпуск')
    f = types.KeyboardButton(text='🍽 Где поесть')
    e = types.KeyboardButton(text='🗄 Как найти склад и отдел кадров')
    g = types.KeyboardButton(text='💰 Зарплатный проект')
    h = types.KeyboardButton(text='ℹ️ ДМС')
    n = types.KeyboardButton(text='♦️ Скидки')
    j = types.KeyboardButton(text='💬 Ответы на Вопросы')
    markup.add(a)
    markup.add(b, c, d)
    markup.add(e)
    markup.add(g)
    markup.add(f, h, n)
    markup.add(j)
    return markup

def back_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = types.KeyboardButton("⏪ Главное меню")
    markup.add(main_menu)
    return markup

def check_users_employee():
    global id_user
    with open('managers_and_employees.txt', 'r', encoding="utf-8") as f:
        for line in f.readlines():
            id_people = line.split()[1]
            if str(id_user) == id_people:
                return True
        else:
            return False

def get_name_admin(password):
    global manager_name
    with open('main_file.txt', 'r', encoding="utf-8") as f:
        for line in f.readlines():
            try:
                if line.split('-')[0] == password:
                    manager_name = line.split('-')[1]
            except Exception:
                pass


def admin_check_password(message):
    if message.text in work_file_main("passwords") or message.text == "yardez_comrade" or message.text == "COMRADE":
        get_name_admin(message.text)
        bot.send_message(message.chat.id, text="✅ Доступ Получен 🔓\n├ Теперь можете использовать меню\n└ Выберите что хотите.", reply_markup=admin_panel())
    elif message.text == "⏪ Главное меню":
        bot.send_message(message.chat.id, text="◾️ Вы перешли в главное меню ⤵️\nПривет, {0.first_name} 👋!\nДавай познакомимся ✨".format(message.from_user), reply_markup=start_markup_choose())
    else:
        bot.send_message(message.chat.id, text="❌ Ключа не существует 🔒\n├Либо срок ключа истёк ⏳\n└Попробуйте снова 🔐", reply_markup=back_main_menu())
        bot.register_next_step_handler(message, admin_check_password)
        bot.send_message(message.chat.id, text="🔑 Введите пароль: ")

def print_employees_manegers(message):
    global manager_name
    employees = ''
    with open('managers_and_employees.txt', 'r', encoding="utf-8") as f:
        for line in f.readlines():
            #print(line.split()[1], line.split()[2], line.split()[3])
            if line.split()[0].strip() == manager_name.strip():
                # print(line.split()[1], line.split()[2], line.split()[3])
                employees += f'\n<================>\n👨‍💻 Пользователь: {line.split()[2]}\n💼 Статус: {line.split()[3]}\n🔸 Айди: {line.split()[1]}'
    bot.send_message(message.chat.id, text=f'👥 Ваши сотрудники:\n{employees}\n<================>')

def telegram_contact_mpp(nickname_telegram):
    keyboard = types.InlineKeyboardMarkup()
    a = types.InlineKeyboardButton(text='Телеграмм моего МПП', url=f'https://t.me/{nickname_telegram}')
    keyboard.add(a)
    return keyboard

def send_all(message):  # Рассылка пользователем
    global manager_name
    users_id_list = []
    with open('managers_and_employees.txt', 'r', encoding="utf-8") as f:
        for line in f.readlines():
            if line.split()[0].strip() == manager_name.strip():
                users_id_list.append(line.split()[1])
        for user in set(users_id_list):  # Дополнительная фильтрация списика !
            if message.text == '⏪ Главное меню':
                bot.send_message(message.chat.id, text="📍 Вы перешли в главное меню.", reply_markup=start_markup_choose())
                break
            else:
                try:
                    bot.send_message(user, text=message.text)
                except Exception:  # В случае не существуещего id пользователя !
                    pass

def get_week(number_week=0):
    count = 1
    weekdays = []
    slovar = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
        7: 'Воскресенье'
    }
    slovar_new = {}
    for i in Week.days(Week.thisweek()+number_week):
        # print(f'{slovar[count]} ===> {i}')
        count += 1
        weekdays.append(f'{i}')
    count, week = 1, 0
    for _ in weekdays:
        slovar_new[slovar[count]] = weekdays[week]
        count += 1
        week += 1
    return slovar_new

def get_name_now_date():
    now_date_main = datetime.datetime.now()
    now_date = str(now_date_main).split()[0]
    print('START')
    days_from_week = get_week()
    for name_days, date in days_from_week.items():
        if now_date.strip() == date.strip():
            return name_days

def send_definite_date_of_time(message):
    global now_date, send_text_tagret_date, send_date, send_time
    while True:
        time.sleep(1)
        print('_________________________')
        print('PROCESS:')
        print('TEXT FOR SANDING: ' + send_text_tagret_date)
        print('NOW DATE AND TIME :' + now_date, now_time)
        print('TARGET DATE AND TIME ===> ' + send_date.strip(), send_time.strip())
        print('_________________________')
        if now_date.strip() == send_date.strip() and now_time.strip() == send_time.strip():
            bot.send_message(message.chat.id, text=send_text_tagret_date)
            break



def Send_First_Day(message):
    bot.send_message(message.chat.id, text=Send_First_Day_first_text, reply_markup=main_menu())
    time.sleep(3600)
    bot.send_message(message.chat.id, text=Send_First_Day_second_text, reply_markup=main_menu())
    time.sleep(3600)
    bot.send_message(message.chat.id, text=Send_First_Day_threed_text)
    Send_Others_FOUR_Days(message)


def Send_Monday_Wend_Fri(message):
    global week_start_send_others_days, send_date, send_time, send_texts_tagrets, send_text_tagret_date
    week_start_send_others_days += 1
    send_text_tagret_date = send_texts_tagrets[0]
    send_date, send_time = get_week(week_start_send_others_days)['Понедельник'], '10:00'
    Thread(target=send_definite_date_of_time(message)).start()
    send_text_tagret_date = send_texts_tagrets[1]
    send_date, send_time = get_week(week_start_send_others_days)['Среда'], '10:00'
    Thread(target=send_definite_date_of_time(message)).start()
    send_text_tagret_date = send_texts_tagrets[2]
    send_date, send_time = get_week(week_start_send_others_days)['Пятница'], '10:00'
    Thread(target=send_definite_date_of_time(message)).start()

def Send_Others_Days(message):
    global week_start_send_others_days, send_texts_tagrets
    send_texts_tagrets = [Send_Monday_Day_SECOND_Week_text, Send_Wendsdays_Day_SECOND_Week_text,
                          Send_Friday_Day_SECOND_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_THREED_Week_text, Send_Wendsdays_Day_THREED_Week_text,
                          Send_Friday_Day_THREED_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_FOURTH_Week_text, Send_Wendsdays_Day_FOURTH_Week_text,
                          Send_Friday_Day_FOURTH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_FIFTH_Week_text, Send_Wendsdays_Day_FIFTH_Week_text,
                          Send_Friday_Day_FIFTH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_SIXTH_Week_text, Send_Wendsdays_Day_SIXTH_Week_text,
                          Send_Friday_Day_SIXTH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_SEVENTH_Week_text, Send_Wendsdays_Day_SEVENTH_Week_text,
                          Send_Friday_Day_SEVENTH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_EIGHTH_Week_text, Send_Wendsdays_Day_EIGHTH_Week_text,
                          Send_Friday_Day_EIGHTH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_NINETH_Week_text, Send_Wendsdays_Day_NINETH_Week_text,
                          Send_Friday_Day_NINETH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_TENH_Week_text, Send_Wendsdays_Day_TENH_Week_text,
                          Send_Friday_Day_TENH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_ELEVENTH_Week_text, Send_Wendsdays_Day_ELEVENTH_Week_text,
                          Send_Friday_Day_ELEVENTH_Week_text]
    Send_Monday_Wend_Fri(message)
    send_texts_tagrets = [Send_Monday_Day_TWELVE_Week_text, Send_Wendsdays_Day_TWELVE_Week_text,
                          Send_Friday_Day_TWELVE_Week_text]
    Send_Monday_Wend_Fri(message)


def Send_Others_FOUR_Days(message):
    global now_date, send_text_tagret_date, send_date, send_time, week_start_send_others_days
    if get_name_now_date() == 'Суббота' or get_name_now_date() == 'Воскресенье':
        print(get_week(1))
        print(get_week(1)['Понедельник'])
        print(get_week(1)['Вторник'])
        print(get_week(1)['Среда'])
        print(get_week(1)['Четверг'])
        send_text_tagret_date = Send_Second_Day_First_Week_text
        send_date, send_time = get_week(1)['Понедельник'], '10:00'
        Thread(target=send_definite_date_of_time(message)).start()
        send_text_tagret_date = Send_Threed_Day_First_Week_text
        send_date, send_time = get_week(1)['Вторник'], '10:00'
        Thread(target=send_definite_date_of_time(message)).start()
        send_text_tagret_date = Send_Foured_Day_First_Week_text
        send_date, send_time = get_week(1)['Среда'], '10:00'
        Thread(target=send_definite_date_of_time(message)).start()
        send_text_tagret_date = Send_Fifth_Day_First_Week_text
        send_date, send_time = get_week(1)['Четверг'], '10:00'
        Thread(target=send_definite_date_of_time(message)).start()
        week_start_send_others_days = 2
        Send_Others_Days(message)
    else:
        print(get_name_now_date())
        if get_name_now_date() == 'Понедельник': # Уникальный Случай
            print(get_week())
            print(get_week()['Вторник'])
            print(get_week()['Среда'])
            print(get_week()['Четверг'])
            print(get_week()['Пятница'])
            send_text_tagret_date = Send_Second_Day_First_Week_text
            send_date, send_time = get_week()['Вторник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Threed_Day_First_Week_text
            send_date, send_time = get_week()['Среда'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Foured_Day_First_Week_text
            send_date, send_time = get_week()['Четверг'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Fifth_Day_First_Week_text
            send_date, send_time = get_week()['Пятница'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            week_start_send_others_days = 1
        elif get_name_now_date() == 'Вторник':
            print(get_week())
            print(get_week()['Среда'])
            print(get_week()['Четверг'])
            print(get_week()['Пятница'])
            print(get_week(1)['Понедельник'])
            send_text_tagret_date = Send_Second_Day_First_Week_text
            send_date, send_time = get_week()['Среда'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Threed_Day_First_Week_text
            send_date, send_time = get_week()['Четверг'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Foured_Day_First_Week_text
            send_date, send_time = get_week()['Пятница'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Fifth_Day_First_Week_text
            send_date, send_time = get_week(1)['Понедельник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            week_start_send_others_days = 2
        elif get_name_now_date() == 'Среда':
            print(get_week())
            print(get_week()['Четверг'])
            print(get_week()['Пятница'])
            print(get_week(1)['Понедельник'])
            print(get_week(1)['Вторник'])
            send_text_tagret_date = Send_Second_Day_First_Week_text
            send_date, send_time = get_week()['Четверг'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Threed_Day_First_Week_text
            send_date, send_time = get_week()['Пятница'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Foured_Day_First_Week_text
            send_date, send_time = get_week(1)['Понедельник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Fifth_Day_First_Week_text
            send_date, send_time = get_week(1)['Вторник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            week_start_send_others_days = 2
        elif get_name_now_date() == 'Четверг':
            print(get_week())
            print(get_week()['Пятница'])
            print(get_week(1)['Понедельник'])
            print(get_week(1)['Вторник'])
            print(get_week(1)['Среда'])
            send_text_tagret_date = Send_Second_Day_First_Week_text
            send_date, send_time = get_week()['Пятница'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Threed_Day_First_Week_text
            send_date, send_time = get_week(1)['Понедельник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Foured_Day_First_Week_text
            send_date, send_time = get_week(1)['Вторник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Fifth_Day_First_Week_text
            send_date, send_time = get_week(1)['Среда'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            week_start_send_others_days = 2
        elif get_name_now_date() == 'Пятница':
            print(get_week())
            print(get_week(1)['Понедельник'])
            print(get_week(1)['Вторник'])
            print(get_week(1)['Среда'])
            print(get_week(1)['Четверг'])
            send_text_tagret_date = Send_Second_Day_First_Week_text
            send_date, send_time = get_week(1)['Понедельник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Threed_Day_First_Week_text
            send_date, send_time = get_week(1)['Вторник'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Foured_Day_First_Week_text
            send_date, send_time = get_week(1)['Среда'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            send_text_tagret_date = Send_Fifth_Day_First_Week_text
            send_date, send_time = get_week(1)['Четверг'], '10:00'
            Thread(target=send_definite_date_of_time(message)).start()
            week_start_send_others_days = 2
        Send_Others_Days(message)


@bot.message_handler(commands=['start', 'Start'])
def start(message):
    global id_user, employee_status, username_user, flag_begin_time
    username_user = message.from_user.username
    id_user = message.from_user.id
    def get_now_date():
        global now_date, now_time
        while True:
            time.sleep(1)
            now_date_main = datetime.datetime.now()
            now_date = str(now_date_main).split()[0]
            now_time = str(now_date_main).split()[1].split('.')[0].split(':')
            now_time.pop(-1)
            now_time = ':'.join(now_time)
            print('NOW: '+ now_date, now_time)
    if flag_begin_time == False:
        daemon = Thread(target=get_now_date, daemon=True, name='Background')
        daemon.start()
        flag_begin_time = True

    if check_users_employee():
        bot.send_message(message.chat.id,
                        text="🚀 Добро пожаловать {0.first_name} в команду Первых 👋 !".format(message.from_user),
                        reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, text="👋 Привет, {0.first_name} !\nДавай познакомимся ✨".format(message.from_user), reply_markup=start_markup_choose())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global employee_status, id_user
    if call.data == 'employee':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,
                         text="🚀 Добро пожаловать {0.first_name} в команду Первых !\nТы офисный сотрудник или работаешь удаленно?".format(call.message.from_user),
                         reply_markup=markup_choose_employee())
    elif call.data == 'admin':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,text="🚀 Добро пожаловать {0.first_name} !\n🔐 Напиши свой персональный код.".format(call.message.from_user))
        bot.send_message(call.message.chat.id, text="🔑 Введите пароль: ", reply_markup=back_main_menu())
        bot.register_next_step_handler(call.message, admin_check_password)
    elif call.data == 'send_panel':
        bot.send_message(call.message.chat.id,
                         "⚠️РАССЫЛКА ⛔\n Введите текст который хотите вывести либо выйдите в главное меню !",
                         reply_markup=back_main_menu())
        bot.register_next_step_handler(call.message, send_all)
    elif call.data == 'print_users':
        print_employees_manegers(call.message)
    elif call.data == 'office':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        employee_status = 'Офисный'
        print(employee_status)
        bot.send_message(call.message.chat.id, text="🧑‍💻 Кто твой менеджер из отдела персонала ?", reply_markup=manegers_names())
    elif call.data == 'remote':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        print(employee_status)
        employee_status = 'Удалённый'
        bot.send_message(call.message.chat.id, text="🧑‍💻 Кто твой менеджер из отдела персонала ?", reply_markup=manegers_names())
    elif call.data == 'manager1' or call.data == 'manager2' or call.data == 'manager3' or call.data == 'manager4' or call.data == 'manager5' or call.data == 'manager6' or call.data == 'manager7' or call.data == 'manager8':
        global username_user
        bot.delete_message(call.message.chat.id, call.message.message_id)
        with open('managers_and_employees.txt', 'a', encoding="utf-8") as f:
            if call.data == 'manager1':
                name_maneger = 'Марина'
            elif call.data == 'manager2':
                name_maneger = 'Анна'
            elif call.data == 'manager3':
                name_maneger = 'Лиза'
            elif call.data == 'manager4':
                name_maneger = 'Виктория'
            elif call.data == 'manager5':
                name_maneger = 'Дарья'
            elif call.data == 'manager6':
                name_maneger = 'Юлия'
            elif call.data == 'manager7':
                name_maneger = 'Елена'
            elif call.data == 'manager8':
                name_maneger = 'Наталья'
            print(f'{name_maneger} {id_user} @{username_user} {employee_status}')
            f.write(f'\n{name_maneger} {id_user} @{username_user} {employee_status}')
        bot.send_message(call.message.chat.id,
                        text=f"🚀 Добро пожаловать {username_user} в команду Первых 👋 !",
                        reply_markup=main_menu())
        Send_First_Day(call.message)

@bot.message_handler(content_types=['text'])
def main(message):
    global employee_status
    id_user = message.from_user.id
    if message.text == "☎️ Контакт моего МПП":
        with open('managers_and_employees.txt', 'r', encoding="utf-8") as f:
            for line in f.readlines():
                id_people = line.split()[1]
                if str(id_user) == id_people:
                    name_maneger = line.split()[0]
        if name_maneger == 'Юлия':
            bot.send_message(message.chat.id, text="👩‍💻 Юлия Казачкова - Ведущий менеджер по персоналу\n📞 Внутренний номер: 1480\n🌐 Почта: UAnpilova@1cbit.ru\n📩 Телеграм: @hdhfhgd ⤵️", reply_markup=telegram_contact_mpp('@hdhfhgd'))
        elif name_maneger == 'Елена':
            bot.send_message(message.chat.id, text="👩‍💻 Елена Донская - Ведущий менеджер по персоналу (удалённый сотрудник)\n📞 Внутренний номер: 1586\n🌐 Почта: ENDonskaya@1cbit.ru\n📩 Телеграм: @Elena_Dons ⤵️", reply_markup=telegram_contact_mpp('@Elena_Dons'))
        elif name_maneger == 'Анна':
            bot.send_message(message.chat.id, text="👩‍💻 Анна Павлова - Ведущий менеджер по персоналу\n📞 Внутренний номер: 1649\n🌐 Почта: AnUPavlova@1cbit.ru\n📩 Телеграм: @anpavlova7 ⤵️", reply_markup=telegram_contact_mpp('@anpavlova7'))
        elif name_maneger == 'Наталья':
            bot.send_message(message.chat.id, text="👩‍💻 Наталья Ваганова - Ведущий менеджер по персоналу (удалённый сотрудник)\n📞 Внутренний номер: 1649\n🌐 Почта: NMVaganova@1cbit.ru ⤵️")
        elif name_maneger == 'Лиза':
            bot.send_message(message.chat.id, text="👩‍💻 Лиза Амирян - Менеджер по персоналу\n📞 Внутренний номер: 1216\n🌐 Почта: LAAmiryan@1cbit.ru\n📩 Телеграм: @laa_afrodita ⤵️", reply_markup=telegram_contact_mpp('@laa_afrodita'))
        elif name_maneger == 'Марина':
            bot.send_message(message.chat.id, text="👩‍💻 Марина Архипова - Менеджер по персоналу\n📞 Внутренний номер: 1471\n🌐 Почта: MAArkhipova@1cbit.ru\n📩 Телеграм: @marinaarkhipovaa ⤵️", reply_markup=telegram_contact_mpp('@marinaarkhipovaa'))
        elif name_maneger == 'Дарья':
            bot.send_message(message.chat.id, text="👩‍💻 Дарья Казимирская - Менеджер по персоналу\n📞 Внутренний номер: 1340\n🌐 Почта: DKKazimirskaya@1cbit.ru\n📩 Телеграм: @daryathaumiel ⤵️", reply_markup=telegram_contact_mpp('@daryathaumiel'))
        elif name_maneger == 'Виктория':
            bot.send_message(message.chat.id, text="👩‍💻 Виктория Флоря - Менеджер по персоналу\n📞 Внутренний номер: 1354\n🌐 Почта: VIFlorya@1cbit.ru\n📩 Телеграм: @floryav ⤵️", reply_markup=telegram_contact_mpp('@floryav'))
    elif message.text == "💠 Ресепшн":
        bot.send_message(message.chat.id, text="""
💠 Наши секретари на ресепшн всегда готовы помочь тебе по вопросам доставки документов, 
оформления пропуска и бейджа. Также там находится аптечка, фирменные пакеты и вкусный чай с кофе. ☕️
👩‍💼 Наши секретари: 
• Анастасия Грачёва и Светлана Комаристая - Секретари ресепшн 
• Внутренние номера: 1178, 1213
• Почта: welcome_CO@1cbit.ru
""")
    elif message.text == "📑 Справки":
        keyboard = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(text='🔗 Ссылка', url=f'https://newportal.1cbit.ru/knowledge/portal_instruktsii/zup31/')
        keyboard.add(a)
        bot.send_message(message.chat.id, text="""
📑 Различные справки (2-НДФЛ, справка с места работы и т.д.) можно заказать через наш корпоративный портал. 🌐
📄 Через портал ты попадёшь в кабинет самообслуживания в 1С:ЗУП 3.1. Внимательно изучи инструкцию по использованию программы! """, reply_markup=keyboard)
    elif message.text == "✈️ Отпуск":
        keyboard = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(text='🔗 Ссылка', url=f'https://newportal.1cbit.ru/knowledge/portal_instruktsii/zup31/')
        keyboard.add(a)
        bot.send_message(message.chat.id, text="""
✈️ Отпуск или командировку можно оформить через наш корпоративный портал. 
🌐 Через портал ты попадёшь в кабинет самообслуживания в программе 1С:ЗУП 3.1. 
Внимательно изучи инструкцию по использованию программы!""", reply_markup=keyboard)
    elif message.text == "🍽 Где поесть":
        keyboard = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(text='🗺 На картах', url=f'https://yandex.ru/maps/?um=constructor%3A5f9d9adab3e8173f8e457039f52e46f9b5a9979409437a17eb42a28a001438e4&source=constructorLink')
        keyboard.add(a)
        bot.send_photo(message.chat.id, 'https://ibb.co/R233LJJ', caption="""
🏢 Рядом с офисом есть много классных мест, в которых можно пообедать или провести время с коллегами после работы. 😎 
📋 Мы составили список самых популярных!""", reply_markup=keyboard)
    elif message.text == "🗄 Как найти склад и отдел кадров":
        keyboard = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(text='🗺 На картах',url=f'https://yandex.ru/maps/?um=constructor%3Acd8b9e3a2cba17550e4c8ff132367fd80a4f0afc4a8e21f6e9cb48a5cfdb7c75&source=constructorLink')
        keyboard.add(a)
        bot.send_message(message.chat.id, text="""
🗄 Отправили на склад за ноутбуком, а адрес не подсказали? 
🗺 Наша карта поможет тебе найти всё самое необходимое: склад, ЦКП, отдела кадров.""",
                 reply_markup=keyboard)
    elif message.text == "💰 Зарплатный проект":
        keyboard = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(text='🔗 Ссылка',
                                       url=f'https://confluence.1cbit.ru/pages/viewpage.action?pageId=56116195')
        keyboard.add(a)
        bot.send_message(message.chat.id, text="""
ℹ️ С информацией по зарплатному проекту Первого бита можно ознакомиться на нашем корпоративном портале.""",
                 reply_markup=keyboard)
    elif message.text == "ℹ️ ДМС":
        keyboard = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(text='🔗 Ссылка',
                                       url=f'https://confluence.1cbit.ru/pages/viewpage.action?pageId=56116193')
        keyboard.add(a)
        bot.send_message(message.chat.id, text="""
ℹ️ С информацией по льготному ДМС в компании можно ознакомиться на корпоративном портале. 
Если остались какие-то вопросы - их можно задать Инне Петровой, ответственному за ДМС специалисту.
• Внутренний номер: 3877
• Эл. почта: IAPetrova@1cbit.ru
""", reply_markup=keyboard)
    elif message.text == "♦️ Скидки":
        keyboard = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(text='🔗 Ссылка',
                                       url=f'https://newportal.1cbit.ru/employees/promotions/')
        keyboard.add(a)
        bot.send_message(message.chat.id, text="""
♦️ У нас много разных скидок и предложений от партнёров: фитнес, иностранные языки, магазины, рестораны, отели. 
Обязательно посмотри на портале все предложения.""", reply_markup=keyboard)
    elif message.text == "💬 Ответы на Вопросы":
        bot.send_message(message.chat.id, text="""
💬 Ответы на вопросы:
==========================
🔸 Есть техническая проблема, что-то сломалось/не работает, к кому обращаться? ❓ 
- <em> По всем техническим проблемам от 1С до принтеров нужно написать письмо с описанием проблемы на 4444@1cbit.ru. </em>
🔸 Где взять ручки, блокноты, кармашек или ленту для пропуска ❓ 
- <em> Вся брендированная канцелярия находится в отделе персонала, каб. №1. Достаточно просто зайти и взять, что тебе нужно! </em>
🔸 Можно ли перепечатать бейджик ❓
- <em> Можно, за этим обращайся на ресепшен. </em>
🔸 Как попасть в отдел кадров ❓
- <em> Отдел кадров находится в одном здании с ЦО, но в другом подъезде. Выходя из ЦО нужно пройти направо до начала здания, зайти в Торгово-офисный центр.\nОтдел кадров находится на 4 этаже, 15 кабинет. </em>
👩‍💼 Светлана Казакова - Ведущий инспектор по кадрам
• Внутренний номер: 3976
• Почта: SSKazakova@1cbit.ru
• <a href="https://yandex.ru/maps/?um=constructor%3Acd8b9e3a2cba17550e4c8ff132367fd80a4f0afc4a8e21f6e9cb48a5cfdb7c75&source=constructorLink">🗺 На картах</a> 
🔸 Как попасть на склад ❓
- <em> Выходя из ЦО нужно пойти налево до арки со шлагбаумом рядом с кофейней "Синкопа". Зайди за шлагбаум и увидишь здание с табличкой "Онлайн-касса", в самом здании нужно повернуть налево.</em>
• <a href="https://yandex.ru/maps/?um=constructor%3Acd8b9e3a2cba17550e4c8ff132367fd80a4f0afc4a8e21f6e9cb48a5cfdb7c75&source=constructorLink">🗺 На картах</a> 
🔸 Мой знакомый хочет работать в Первом бите. Как мне ему помочь ❓
- <em> Передай резюме знакомого менеджерам по персоналу в каб. №1, его обязательно возьмут в работу. </em>
==========================
""", parse_mode='HTML')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)