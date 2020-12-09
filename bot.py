import telebot
import config
from telebot import types
import random

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):

    #Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Cлучайное число")
    item2 = types.KeyboardButton("😃 Как дела?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!\nЯ - принц <b>{1.first_name}</b>, бот ".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Cлучайное число':
            bot.send_message(message.chat.id, "Твоё случаное число " + str(random.randint(0, 100)))
        elif message.text == "😃 Как дела?":

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Так себе", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Всё круто, а у тебя?", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Я не знаю, как тебе ответить(")
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Это отлично, так держать!')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Всё пройдёт, не беспокойся!')

            # Удаление этой кнопки
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='😃 Как дела?', reply_markup=None)

            #Уведомление
            #bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text="Тебе новое уведомление!")

    except Exception as e:
        print(repr(e))
bot.polling(none_stop=True)
