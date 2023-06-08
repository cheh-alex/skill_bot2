from . import bot


@bot.message_handler(commands=['low', 'high','custom'])
def basic_handler(m):
    if m.text == '/low':
        bot.send_message(m.chat.id, 'Выборка товаров с низкой ценой.')
    elif m.text == '/high':
        bot.send_message(m.chat.id, 'Выборка товаров с высокой ценой.')
    elif m.text == '/custom':
        bot.send_message(m.chat.id,'Вы выбрали кастомную филь-цию')

