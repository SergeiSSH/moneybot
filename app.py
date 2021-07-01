import telebot
from tkeys import keys, TOKEN
from extensions import ConvertionException, CryptoConvertion

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Начните работу введя команду в формате: \n <имя валюты> <в какую валюту перевести> <кол-во валюты> \n "Увидеть список доступных валют: /value"'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n-'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное кол-во параметров!')
        quote, base, amount = values
        total_base = CryptoConvertion.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка обработки команд\n{e}')
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} на данный момент {round(float(total_base) * float(amount), 4)}'
        bot.send_message(message.chat.id, text)


bot.polling()
