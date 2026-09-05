import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton


def is_address(w):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent='my_city_checker')
    location = geolocator.geocode(w, timeout=10, language="ru")
    return location


bot = telebot.TeleBot('6646359255:AAGtAGwG-O4I20TBe8OqtjLtjJA5MVS6qss')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Введите свой город/район/примерный адрес'
    )


@bot.message_handler(func=lambda message: True)
def get_city(message: Message):
    from json_manager import get_all

    if str(message.chat.id) in get_all():
        handle_buttons(message)
        return

    address = is_address(message.text)
    if address:
        from json_manager import new_chat
        new_chat(message.chat.id, (address.latitude, address.longitude))

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = KeyboardButton('Узнать погоду')
        btn2 = KeyboardButton('Сменить адрес')
        keyboard.add(btn1, btn2)

        bot.send_message(
            message.chat.id,
            'Отлично!',
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            'Похоже это не город'
        )


def handle_buttons(message):
    chat_id = message.chat.id
    text = message.text

    if text == 'Узнать погоду':
        from json_manager import get_address
        from weather import get_forecast

        f = get_forecast(*get_address(str(chat_id)))
        if f:
            m = f'Погода сейчас:\n\tТемпература: {f.temperature}\n\tСкорость ветра: {f.wind_speed}\n\tНаправление ветра: {f.wind_direction}'
            bot.reply_to(message, m)
        else:
            bot.reply_to(message, 'Прогноз погоды не найден')

    elif text == 'Сменить адрес':
        from json_manager import del_address
        del_address(chat_id)

        bot.reply_to(message, 'Введите свой новый город/район/примерный адрес')


if __name__ == '__main__':
    bot.infinity_polling()
