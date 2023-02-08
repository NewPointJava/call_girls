from datetime import datetime, date, timedelta
from settings import check_in_price, room_price, bathroom_price, check_in_time, room_time, bathroom_time, \
    cleaning_frequency_and_discount_dict, extra_name_hour_cost_dict
from translate_func import translate_month, translate_day_of_the_week


def cost_calculation_st1(call_data):
    call_data = call_data.split("*")
    room_amount = int(call_data[1])
    bathroom_amount = int(call_data[2])

    ending_bathroom = ["санузел", "санузла", "санузлов"]

    if room_amount <= 1:
        ending_room = "комната"
    elif 1 < room_amount < 5:
        ending_room = "комнаты"
    elif 5 <= room_amount:
        ending_room = "комнат"

    if bathroom_amount <= 1:
        ending_bathroom = "санузел"
    elif 1 < bathroom_amount < 5:
        ending_bathroom = "санузла"
    elif 5 <= bathroom_amount:
        ending_bathroom = "санузлов"

    cost_1st = check_in_price + room_amount * room_price + bathroom_amount * bathroom_price

    new_text = f'{room_amount} - {ending_room} {bathroom_amount} - {ending_bathroom} = {cost_1st}р'

    return new_text, room_amount, bathroom_amount


def order_card(call_data, time_order, cleaning_frequency_int):
    call_data = call_data.split("$")
    call_data = call_data[1].split("*")
    room_amount = int(call_data[0])
    bathroom_amount = int(call_data[1])

    time_order = time_order.split(" ")
    time_order[0] = translate_day_of_the_week(time_order[0])
    time_order[1] = translate_month(time_order[1])
    time_order = time_order[0] + " " + str(int(time_order[3]) + 1) + " " + time_order[1] + " 08:00"

    if room_amount <= 1:
        ending_room = "жилой"
    elif 1 < room_amount:
        ending_room = "жилыми"

    if bathroom_amount <= 1:
        ending_bathroom = "ванной"
    elif 1 < bathroom_amount:
        ending_bathroom = "ванными"

    cleaning_time = check_in_time + room_amount*room_time + bathroom_amount*bathroom_time
    if cleaning_time % 1 == 0:
        cleaning_time = int(cleaning_time)

    cleaning_frequency = cleaning_frequency_and_discount_dict[str(cleaning_frequency_int)]
    discount_percent = cleaning_frequency[1]
    print(discount_percent)
    cleaning_frequency = cleaning_frequency[0]
    standart_price = check_in_price + room_amount * room_price + bathroom_amount * bathroom_price
    text = f'Уборка квартиры с {room_amount} {ending_room} и {bathroom_amount} {ending_bathroom} комнатами\n\n'\
            f'Дата уборки: {time_order}\n'\
            f'Время уборки: ~ {cleaning_time} ч.\n'\
            f'Регулярность: {cleaning_frequency}\n'\
            f'Стандарнатная стоимость: {standart_price}р'
    final_price = standart_price
    discount_amount = round(final_price*discount_percent, 2)
    if discount_percent > 0:
        text+= f'\nСумма скидки за регулярность: {discount_amount}руб'

    final_price = final_price - discount_amount
    text += f'\nК оплате: {final_price-discount_percent}р'
    return text, room_amount,bathroom_amount


def edit_order_caption_date(caption, cleaning_date):
    caption = caption.split("\n")
    date_and_time = caption[2]
    date_and_time = date_and_time.split(" ")
    cleaning_date = cleaning_date.strftime("%b %a %d")
    cleaning_date = str(cleaning_date)
    cleaning_date = cleaning_date.split(" ")
    print(cleaning_date)
    cleaning_date[0] = translate_month(cleaning_date[0])
    cleaning_date[1] = translate_day_of_the_week(cleaning_date[1])
    cleaning_date = cleaning_date[1] + " " + cleaning_date[2] + " " + cleaning_date[0]
    caption[2] = f'Дата уборки: {cleaning_date} {date_and_time[-1]}'
    new_caption = "\n".join(caption)
    return new_caption


def edit_order_caption_time(caption, cleaning_time):
    caption = caption.split("\n")
    date_and_time = caption[2]
    date_and_time = date_and_time.split(" ")
    date_and_time[-1] = cleaning_time
    date_and_time = " ".join(date_and_time)
    caption[2] = date_and_time
    new_caption = "\n".join(caption)

    room_and_bathroom_amount = caption[0]
    room_and_bathroom_amount = room_and_bathroom_amount.split(" ")
    room_amoun = int(room_and_bathroom_amount[3])
    bathroom_amount = int(room_and_bathroom_amount[6])
    return new_caption, room_amoun, bathroom_amount

def edit_caption_extra_service(caption, call_data):
    caption = caption.split("\n")
    sign = call_data[-1]
    service_key = call_data.split("$")
    service_key = service_key[1][:2]
    standart_price_pos = 0
    hour = 0
    for i in range(len(caption)-1):
        if "Стандарнатная стоимость" in caption[i]:
            standart_price_pos = i

    standart_price = caption[standart_price_pos].split(" ")
    standart_price = int(standart_price[-1].replace('р', ""))

    old_time = caption[3]
    old_time.split(" ")
    for i in range(len(old_time) - 1):
        if old_time[i].isdigit():
            hour = int(old_time[i])




    if sign =="+":
        if "Дополнительные услуги" not in caption[standart_price_pos + 1]:
            caption.insert(standart_price_pos+1, "Дополнительные услуги")
            caption.insert(standart_price_pos + 2, "Стоимость уборки с дополнительными услугами:")
        caption.insert(standart_price_pos+2, extra_name_hour_cost_dict[service_key][0] + ": " + str(extra_name_hour_cost_dict[service_key][2]))
        hour += extra_name_hour_cost_dict[service_key][1]
    else:
        hour -= extra_name_hour_cost_dict[service_key][1]
        for i in range(standart_price_pos+1, len(caption)-1):
            if extra_name_hour_cost_dict[service_key][0] in caption[i]:
                caption.pop(i)
        amount_extra = 0
        for i in range(standart_price_pos+2, len(caption)-2):
            if "Стоимость уборки с дополнительными:" not in caption[i]:
                amount_extra += 1
        if amount_extra == 0:
            caption.pop(standart_price_pos+1)
            caption.pop(len(caption)-2)


    caption[3] = "Время уборки: ~ " + str(hour) + " ч."

    if "Стоимость уборки с дополнительными" in caption[-2]:
        extra_price = 0
        for i in range(standart_price_pos+2, len(caption)-2):
            price = caption[i].split(" ")
            print(price)
            price = int(price[-1])
            extra_price += price
        caption[-2] = "Стоимость уборки с дополнительными услугами: " + str(standart_price + extra_price) +"р"
        caption[-1] = "К оплате: " + str(standart_price + extra_price) +"р"
    else:
        caption[-1] = "К оплате: " + str(standart_price) + "р"

    new_caption = "\n".join(caption)

    return new_caption


def edit_caption_discount(caption, discount_percent):
    caption = caption.split("\n")
    payment = caption[-1]
    payment = payment.split(" ")
    payment = payment[-1].replace("р", "")
    discount = 0
    discount_percent = float(discount_percent)
    standart_price = 0
    extra_price = 0

    for i in range(len(caption)-1):
        if "Стандарнатная стоимость" in caption[i]:
            standart_price = caption[i].split(" ")
            standart_price = int(standart_price[-1].replace("р",""))

        if "Стоимость уборки с дополнительными" in caption[i]:
            extra_price = caption[i].split(" ")
            extra_price = int(extra_price[-1].replace("р", ""))


    if discount_percent == 0:
        for i in range(len(caption)-1):
            if "Сумма скидки за регулярность" in caption[i]:
                discount = caption.pop(i)
                discount = discount.split(" ")
                discount = discount[-1].replace("р", "")
                if extra_price != 0:
                    caption[-1] = "К оплате: " + str(extra_price) + "р"
                else:
                    caption[-1] = "К оплате: " + str(standart_price) + "р"

    else:
        k = 0
        for i in range(len(caption)-1):
            if "Сумма скидки за регулярность" in caption[i]:
                k += 1
                if extra_price != 0:
                    discount = round(extra_price*(discount_percent/100), 2)
                else:
                    discount = round(standart_price*(discount_percent/100), 2)

                caption[i] = "Сумма скидки за регулярность: " + str(discount) + "р"

        if k == 0:
            if extra_price != 0:
                discount = round(extra_price * (discount_percent / 100), 2)
                caption.insert(len(caption)- 1, "Сумма скидки за регулярность: " + str(discount) + "р")

            else:
                discount = round(standart_price * (discount_percent / 100), 2)
                caption.insert(len(caption) - 1, "Сумма скидки за регулярность: " + str(discount) + "р")
        if extra_price != 0:
            caption[-1] = "К оплате: " + str(extra_price-discount) + "р"
        else:
            caption[-1] = "К оплате: " + str(standart_price-discount) + "р"


    new_caption = "\n".join(caption)

    return new_caption