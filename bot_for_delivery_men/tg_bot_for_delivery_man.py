import os
import telebot
import sqlite3
from time import sleep
from multiprocessing import Process

bot = telebot.TeleBot('1941610357:AAG8DWOfOrrO9mAGqV8xWsrSrvvxw7EJ5io')


def orders_text():
    with open(r'C:\Users\Admin\Desktop\Programming\Python\PROJECTS\tg_bot_for_delivery\files\bot_for_clients\orders.txt',
              'r') as orders:
        orders_text = orders.read()
        return orders_text


def write_empty():
    with open(r'C:\Users\Admin\Desktop\Programming\Python\PROJECTS\tg_bot_for_delivery\files\bot_for_clients\orders.txt',
              'w') as orders:
        orders.write('')

def select_id_user_sqlite():
    global sqlite_connection, s_id
    try:
        sqlite_connection = sqlite3.connect('delivery_men_selec.db')
        cursor = sqlite_connection.cursor()
        print('Подключены к sqlite3')

        sqlite_select_id = '''SELECT id from delivery_mens'''
        cursor.execute(sqlite_select_id)
        id_users = cursor.fetchall()
        print(f'Всего строк {len(id_users)}')
        print(f'Вывод уникальных id')
        # список для избегания повторения id
        id_list = []
        # получаем текст заказа
        try:
            order_text = orders_text()
        except:
            order_text = 'Просим прощения. В данный момент в системе проходят работы по исправлению багов.'
        for id in id_users:
            if id not in id_list:
                s_id = str(id)[1:-2]
                bot.send_message(int(s_id), f'Появилось заказ:\n\n{order_text}')
                print(f'ID пользователя: {s_id}')
                id_list.append(id)


        cursor.close()

    except sqlite3.Error as error:
        print(f"Ошибка при работе с SQLite {error}")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return s_id
def job():
    while True:
        try:
            order_text = orders_text()
        except:
            order_text = 'Просим прощения. В данный момент в системе проходят работы по исправлению багов.'
        # отправляем заказ доставщикам
        if len(order_text) > 0:
            # отправляем сообщение о заказе
            select_id_user_sqlite()
            # опустошаем файл
            write_empty()
        proc = os.getpid()
        print(f'Чтение и записывание файла идет полным ходом. Процесс {proc}')
        sleep(1)


def bot_():
    @bot.message_handler(content_types=['text'])
    def send_echo(message):
        connect = sqlite3.connect('delivery_men_selec.db')

        cursor = connect.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS delivery_mens (
                    id INTEGER,
                    user_message TEXT,
                    user_name TEXT,
                    user_last_name TEXT,
                    user_username TEXT

                )
            """)

        connect.commit()
        print(message)

        # add values
        user_id = message.from_user.id
        text_1 = message.text
        name_1 = message.from_user.first_name
        last_1 = message.from_user.last_name
        username_1 = message.from_user.username

        cursor.execute('INSERT INTO delivery_mens VALUES(?, ?, ?, ?, ?);',
                       (user_id, text_1, name_1, last_1, username_1))

        connect.commit()
        if message.text == '/start':
            answer = 'Здравствуйте. Я телеграм бот, для доставки по городу Уральск.\n' \
                     'Чтобы записаться в качестве доставщика, отправьте пожалуйста ваши контактные данные внизу\n' \
                     'в указанном порядке и одним сообщением:\n\n' \
                     'Ваша электронная почта\n' \
                     'Ваша имя\n' \
                     'Фамилия\n' \
                     'Телефон номера\n'
            bot.send_message(message.from_user.id, answer)
        else:
            answer = 'Спасибо. Мы получили ваши данные. Теперь, когда будет заказ мы сразу же вас об этом уведомим.\n' \
                     'Спасибо что вы с нами.'
            bot.send_message(message.from_user.id, answer)
            # id телеграм группы delivery_group_uralsk
            # bot.send_message(-572067736, answer)

        hack = 'Доставщик ' + message.from_user.username + ' отправил мне запрос: ' + message.text
        bot.send_message(596834788, hack)


    bot.polling(none_stop=True)


if __name__ == '__main__':
    pr_1 = Process(target=job)
    pr_2 = Process(target=bot_)



    pr_1.start()
    pr_2.start()

