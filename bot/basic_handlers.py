from . import bot
from .keyboards import create_categories_keyboard
from .history import Query
from .api import get_products_of_category, get_all_categories
from .helpers import create_text

states = {}


@bot.message_handler(commands=['low', 'high', 'custom'])
def basic_handler(m):
    states[m.chat.id] = Query()
    states[m.chat.id].type = m.text
    states[m.chat.id].chat_id = m.chat.id
    if m.text == '/low':
        bot.send_message(m.chat.id, 'Выборка товаров с низкой ценой.Выберите категорию',
                         reply_markup=create_categories_keyboard())
        bot.register_next_step_handler(m, category_handler)
    elif m.text == '/high':
        bot.send_message(m.chat.id, 'Выборка товаров с высокой ценой.Выберите категорию',
                         reply_markup=create_categories_keyboard())
        bot.register_next_step_handler(m, category_handler)
    elif m.text == '/custom':
        bot.send_message(m.chat.id, 'Вы выбрали кастомную филь-цию,укажите диапазон цен.')
        bot.register_next_step_handler(m, price_range_handler)


def price_range_handler(m):
    try:
        p1, p2 = m.text.split('-')
        states[m.chat.id].from_price = int(p1)
        states[m.chat.id].to_price = int(p2)
        bot.send_message(m.chat.id, f'Вы выбрали товары с ценами от {p1} до {p2},выберите категорию.',
                         reply_markup=create_categories_keyboard())
        bot.register_next_step_handler(m, category_handler)
    except:
        bot.send_message(m.chat.id, 'Вы указали не правильно диапазон цен!')
        return


def category_handler(m):
    if m.text not in get_all_categories():
        bot.send_message(m.chat.id, 'Вы указали не верную категорию')
        return
    states[m.chat.id].category = m.text
    bot.send_message(m.chat.id, f'Вы выбрали категорию: {m.text}. Укажите кол-во товаров.')
    bot.register_next_step_handler(m, amount_handler)


def amount_handler(m):
    if not m.text.isdigit():
        bot.send_message(m.chat.id, 'Вы ввели не число')
        return
    amount = int(m.text)
    states[m.chat.id].amount = amount
    products = get_products_of_category(states[m.chat.id].category)
    if states[m.chat.id].type == '/low':
        products.sort(key=lambda x: x['price'])

    elif states[m.chat.id].type == '/high':
        products.sort(key=lambda x: x['price'], reverse=True)

    elif states[m.chat.id].type == '/custom':
        products = list(filter(
            lambda p: states[m.chat.id].from_price <= p['price'] <= states[m.chat.id].to_price, products))

    products = products[0:amount]
    for p in products:
        bot.send_photo(m.chat.id, p['thumbnail'], create_text(p['title'], p['description'], p['price']))

    states[m.chat.id].save()
