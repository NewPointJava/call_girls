from datetime import datetime, timedelta

import telebot

from get_and_set_json_information import get_price_and_time, get_feedbacks_from_json, get_admins_and_cleaners_from_json, \
    get_schedule_from_json, get_empy_order_from_order_0

botToken = '5910446276:AAEmL0yB9IEU3SPwzzUT9BXLmIxdXivBh3s'
bot = telebot.TeleBot(botToken)

room_price, room_time, bathroom_price, bathroom_time, check_in_time, check_in_price = get_price_and_time()
admins, cleaners = get_admins_and_cleaners_from_json()
schedule = get_schedule_from_json()
feedbacks = get_feedbacks_from_json()
empty_order = get_empy_order_from_order_0()

not_verified_orders_list = []
orders = dict()

# Регулярность уборки и скидка (Скидка указана в десятичных значениях)
cleaning_frequency_and_discount_dict = dict(
    {"4": ["1 раз или первый раз", 0], "2": ["Раз в неделю", 0.15], "3": ["Раз в две недели", 0.10],
     "1": ["Раз в месяц", 0.07]})

extra_name_hour_cost_dict = dict({
    "fr": ["Внутри холодильника", 1, 25],
    "ov": ["Внутри духовки", 1, 25],
    "kc": ["Внутри кухонных шкафов", 1, 25],
    "ds": ["Помоем посуду", 0.5, 10],
    "mv": ["Внутри микроволновки", 0.5, 20]
})

empty_day = []
hour = datetime.strptime("08:00", "%H:%M")
for i in range(28):
    temp = hour.strftime("%H:%M")
    empty_day.append([temp, True])
    hour = hour + timedelta(minutes=30)



empty_feedback = dict({
    "name": None,
    "text": None,
    "date": None,
    "cleaner": None,
    "order_id": None
})
