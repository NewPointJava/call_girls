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
extra_name_hour_cost_dict = dict({
    "fr": ["Внутри холодильника", 1, 25],
    "ov": ["Внутри духовки", 1, 25],
    "kc": ["Внутри кухонных шкафов", 1, 25],
    "ds": ["Помоем посуду", 0.5, 10],
    "mv": ["Внутри микроволновки", 0.5, 20]
})
