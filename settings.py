import telebot

botToken = '5910446276:AAG-m8VtYrSTRlnyeufAHOZsAIbOXFpgZUs'
bot = telebot.TeleBot(botToken)

room_price = 14
bathroom_price = 20
check_in_price = 31

room_time = 1
bathroom_time = 0.5
check_in_time = 1.5

#Регулярность уборки и скидка (Скидка указана в десятичных значениях)
cleaning_frequency_and_discount_dict = dict({"4": ["1 раз или первый раз", 0], "2": ["Раз в неделю", 0.15], "3": ["Раз в две недели", 0.10], "1": ["Раз в месяц", 0.07]})
