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

empty_order = get_empy_order_from_order_0()

empty_feedback = dict({
    "text": None,
    "date": None,
    "cleaner": None,
    "order_id": None
})

not_verified_orders_list.append([1, dict({
    "order_info": {
        "room": 1,
        "bathroom": 1,
        "date": "Пт 10 Фев",
        "time": "10:00",
        "cleaning_time": 3,
        "frequency": "1 раз или первый раз",
        "standart_price": 10,
        "extra_service": [],
        "extra_price": None,
        "discount_amount": None,
        "payment": 10
    },
    "address": {
        "street": "111",
        "house": "1111",
        "flat": "11111"
    },
    "contact_info": {
        "name": "name1",
        "tel": "tel1",
        "email": "email1"
    },
    "user_id": 1111111,
    "user_name": "Serj_you"
})])

not_verified_orders_list.append([2, dict({
    "order_info": {
        "room": 2,
        "bathroom": 2,
        "date": "Пт 10 Фев",
        "time": "14:00",
        "cleaning_time": 4,
        "frequency": "1 раз или первый раз",
        "standart_price": 20,
        "extra_service": [],
        "extra_price": None,
        "discount_amount": None,
        "payment": 20
    },
    "address": {
        "street": "222",
        "house": "2222",
        "flat": "22222"
    },
    "contact_info": {
        "name": "name2",
        "tel": "tel2",
        "email": "email2"
    },
    "user_id": 222222,
    "user_name": None
})])

not_verified_orders_list.append([3, dict({
    "order_info": {
        "room": 2,
        "bathroom": 2,
        "date": "CБ 11 Фев",
        "time": "11:00",
        "cleaning_time": 4,
        "frequency": "1 раз или первый раз",
        "standart_price": 20,
        "extra_service": [],
        "extra_price": None,
        "discount_amount": None,
        "payment": 20
    },
    "address": {
        "street": "222",
        "house": "2222",
        "flat": "22222"
    },
    "contact_info": {
        "name": "name2",
        "tel": "tel2",
        "email": "email2"
    },
    "user_id": 222222,
    "user_name": "Serj_you"
})])
not_verified_orders_list.append([4, dict({
    "order_info": {
        "room": 2,
        "bathroom": 2,
        "date": "CБ 11 Фев",
        "time": "11:00",
        "cleaning_time": 4,
        "frequency": "1 раз или первый раз",
        "standart_price": 20,
        "extra_service": [],
        "extra_price": None,
        "discount_amount": None,
        "payment": 20
    },
    "address": {
        "street": "222",
        "house": "2222",
        "flat": "22222"
    },
    "contact_info": {
        "name": "name2",
        "tel": "tel2",
        "email": "email2"
    },
    "user_id": 222222,
    "user_name": "Serj_you"
})])
not_verified_orders_list.append([5, dict({
    "order_info": {
        "room": 2,
        "bathroom": 2,
        "date": "CБ 11 Фев",
        "time": "11:00",
        "cleaning_time": 4,
        "frequency": "1 раз или первый раз",
        "standart_price": 20,
        "extra_service": [],
        "extra_price": None,
        "discount_amount": None,
        "payment": 20
    },
    "address": {
        "street": "222",
        "house": "2222",
        "flat": "22222"
    },
    "contact_info": {
        "name": "name2",
        "tel": "tel2",
        "email": "email2"
    },
    "user_id": 222222,
    "user_name": "Serj_you"
})])
