from datetime import datetime, timedelta

import telebot

botToken = '5910446276:AAEmL0yB9IEU3SPwzzUT9BXLmIxdXivBh3s'
bot = telebot.TeleBot(botToken)

room_price = 14
bathroom_price = 20
check_in_price = 31
admins = [694443138]
cleaners = [694443138, 444908023]

not_verified_orders_list = []
feedbacks = []
room_time = 1
bathroom_time = 0.5
check_in_time = 1.5
orders = dict()

#Регулярность уборки и скидка (Скидка указана в десятичных значениях)
cleaning_frequency_and_discount_dict = dict({"4": ["1 раз или первый раз", 0], "2": ["Раз в неделю", 0.15], "3": ["Раз в две недели", 0.10], "1": ["Раз в месяц", 0.07]})
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
    hour = hour + timedelta(minutes=30)
    temp = hour.strftime("%H:%M")
    empty_day.append([temp, True])
print(empty_day)



schedule = dict()
for x in cleaners:
    schedule[str(x)] = dict()
print(schedule)






empty_order = dict({
    "order_info": {
            "room": None,
            "bathroom": None,
            "date": None,
            "time": None,
            "cleaning_time": None,
            "frequency": None,
            "standart_price": None,
            "extra_service": [],
            "extra_price": None,
            "discount_amount": None,
            "payment": None
                    },
    "address": {
            "street": None,
            "house": None,
            "flat": None
                    },
    "contact_info": {
            "name": None,
            "tel": None,
            "email": None
                    },
    "user_id": None,
    "user_name": None,
    "is_created_by_admin": False
})

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

feedbacks.append(dict({
    "name": "name-1",
    "text": "1-ый отзыв",
    "date": "1-ая дата",
    "cleaner": "1-ый клеанер",
    "order_id": 1
}))



feedbacks.append(dict({
    "name": "name-2",
    "text": "2-ый отзыв",
    "date": "2-ая дата",
    "cleaner": "2-ый клеанер",
    "order_id": 2
}))

feedbacks.append(dict({
    "name": "name-3",
    "text": "3-ый отзыв",
    "date": "3-ая дата",
    "cleaner": "3-ый клеанер",
    "order_id": 3
}))

feedbacks.append(dict({
    "name": "name-4",
    "text": "4-ый отзыв",
    "date": "4-ая дата",
    "cleaner": "4-ый клеанер",
    "order_id": 4
}))

feedbacks.append(dict({
    "name": "name-5",
    "text": "5-ый отзыв",
    "date": "5-ая дата",
    "cleaner": "company",
    "order_id": 5
}))

