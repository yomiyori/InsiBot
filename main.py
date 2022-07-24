import telebot
import random
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="newuser",
    password="12345678",
    database="insibot"
)

if db.is_connected():
    print("Database connected")
def update_lgbt(id, lgbt_result):
    cursor = db.cursor()
    sql = "INSERT INTO profile (id, lgbt_result) VALUES(%s, %s) ON DUPLICATE KEY UPDATE lgbt_result = %s"
    val = (id, lgbt_result, lgbt_result)
    cursor.execute(sql, val)
    db.commit()
def update_cattle(id, cattle_result):
    cursor = db.cursor()
    sql = "INSERT INTO profile (id, cattle_result) VALUES(%s, %s) ON DUPLICATE KEY UPDATE cattle_result = %s"
    val = (id, cattle_result, cattle_result)
    cursor.execute(sql, val)
    db.commit()
def get_lgbt_result(id):
    cursor = db.cursor()
    sql = "SELECT lgbt_result FROM profile WHERE id = %s"
    cursor.execute(sql, (id,))
    return cursor.fetchone()
def get_cattle_result(id):
    cursor = db.cursor()
    sql = "SELECT cattle_result FROM profile WHERE id = %s"
    cursor.execute(sql, (id,))
    return cursor.fetchone()

bot = telebot.TeleBot('5419451019:AAEyeyHGSc3t4y5xTm36RPLmyUl_Olx5_H8')

@bot.message_handler(commands=['start'], content_types=['text'])
def functionStart(message):
    mess = f'Привет, {message.from_user.first_name}, я InsiBot \n Мои доступные команды есть в меню'
    bot.send_message(message.chat.id, mess)

@bot.message_handler(commands=['yesorno'])
def YesOrNo(message):
    randomInt = random.randint(1, 2)
    if "?" not in message.text:
        bot.reply_to(message, "Это не вопрос.")
    else:
        if randomInt == 1:
            bot.reply_to(message, "Да, это правда.")
        else:
            bot.reply_to(message, "Нет, это ложь.")


@bot.message_handler(commands=['randomnumber'])
def RandomNumber(message):
    split = message.text.split()
    numberOfWords = len(split)
    if numberOfWords == 3:
        if message.text.split()[1].isnumeric() and message.text.split()[2].isnumeric():
            firstNumber = message.text.split()[1]
            secondNumber = message.text.split()[2]
            randomNum = random.randint(int(firstNumber), int(secondNumber))
            bot.send_message(message.chat.id, "Случайное число: " + str(randomNum))
        else:
            bot.send_message(message.chat.id, "Это не два числа")
    else:
        bot.send_message(message.chat.id, "Неверный формат")


@bot.message_handler(commands=['info'])
def Info(message):
    infoPercent = random.randint(1, 100)
    bot.send_message(message.chat.id, f"Это правда на {infoPercent}%")


@bot.message_handler(commands=['lgbt'])
def lgbt(message):
    lgbtPercent = random.randint(1, 100)
    update_lgbt(message.chat.id, lgbtPercent)
    bot.send_message(message.chat.id, f"Вы представитель лгбт на {lgbtPercent}%")


@bot.message_handler(commands=['cattle'])
def cattle(message):
    cattlePercent = random.randint(1, 100)
    update_cattle(message.chat.id, cattlePercent)
    bot.send_message(message.chat.id, f"Вы быдло на {cattlePercent}%")

@bot.message_handler(commands=['profile'])
def profile(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} \n Вы быдло на {get_cattle_result(message.chat.id)[0]}% и представитель ЛГБТ на {get_lgbt_result(message.chat.id)[0]}%')
@bot.message_handler()
def PingKing(message):
    if message.text == "Пинг":
        bot.reply_to(message, "Понг")
    if message.text == "Кинг":
        bot.reply_to(message, "Конг")
bot.polling(none_stop=True)