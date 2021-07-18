import telebot
import sqlite3

bot = telebot.TeleBot('TOKEN')



@bot.message_handler(content_types=['text'])
def send_echo(message):
    connect = sqlite3.connect('delivery_selec.db')

    cursor = connect.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
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

    cursor.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', (user_id, text_1, name_1, last_1, username_1))

    connect.commit()
    if message.text == '/start':
        answer = 'Здравствуйте. Я телеграм бот, для доставки по городу Уральск.\n' \
                 'Чтобы сделать сделать заказ напишите текст заказа внизу'
        bot.send_message(message.from_user.id, answer)
    else:
        answer = 'Спасибо. Ваш заказ отправлен для всех зарегистрированных в нашей система курьерам.\n' \
            'Ожидайте ответа.'
        bot.send_message(message.from_user.id, answer)

    # hack = 'Пользователь ' + message.from_user.username + ' отправил мне запрос: ' + message.text
    # bot.send_message(596834788, hack)

    with open('orders.txt', 'w') as orders:
        str_order = message.text + ' Заказ от: ' + message.from_user.username
        orders.write(str_order)


bot.polling(none_stop=True)
