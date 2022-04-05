import telebot
from config import keys_2, TOKEN
from Utilss import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def start_(message: telebot.types.Message):
	text = "Введите через пробел команду в следующем формате:\nназвание валюты №1 \nназвание валюты №2, в которой надо узнать цену валюты №1 \nколичество валюты №1.\n\nНапример:\nДоллар Рубль 23\n\nДоступные валюты можно узнать через команду /values"
	bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values_(message: telebot.types.Message):
	text = 'Список доступных валют:\n'
	for key in keys_2.keys():
		text = '\n'.join((text, key))
	bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
	try:
		values_ = message.text.split(' ')

		if len(values_) != 3:
			raise ConvertionException('Некорректный ввод запроса')

		quote, base, amount = values_
		total_base = CryptoConverter.convert_2(quote, base, amount)
	except ConvertionException as e:
		bot.reply_to(message, f'Извините\n{e}')
	except Exception as e:
		bot.reply_to(message, f'Не удалось обработать команду\n{e}')
	else:
		new_price = round((float(amount) * float(total_base)), 2)
		text = f'Цена {amount} {quote} в {base} - {new_price}'
		bot.send_message(message.chat.id, text)

bot.infinity_polling()

