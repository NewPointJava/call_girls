import telebot

botToken = '5910446276:AAEmL0yB9IEU3SPwzzUT9BXLmIxdXivBh3s'
bot = telebot.TeleBot(botToken)

room_price = 14
bathroom_price = 20
check_in_price = 31
admins = [694443138]

not_verified_orders_list = []
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
    "user_name": None
})

test_text = """
Уборка квартиры с 1 жилой и 1 ванной комнатами

Дата уборки: Вс 19 Фев 14:00
Время уборки: ~ 4.0 ч.
Регулярность: 1 раз или первый раз
Стандарнатная стоимость: 65р
Дополнительные услуги
Помоем посуду: 10
Внутри микроволновки: 20
Стоимость уборки с дополнительными услугами: 95р
Сумма скидки за регулярность: 9.5р
К оплате: 85.5р

Адрес
Улица: Минск
Дом: 35
Квартира: 55

Контактная информация
ФИО: Козлов Сергей
Телефон: 367831132
Email: brest@dasas
"""

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
