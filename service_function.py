import json
from datetime import datetime, date, timedelta

from telebot.types import InlineKeyboardMarkup

from get_and_set_json_information import set_schedule_to_json
from settings import check_in_price, room_price, bathroom_price, check_in_time, room_time, bathroom_time, \
    cleaning_frequency_and_discount_dict, extra_name_hour_cost_dict, empty_order, admins, feedbacks, cleaners, \
    not_verified_orders_list, schedule, empty_day
import locale

locale.setlocale(category=locale.LC_ALL, locale="Russian")


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


def order_card(call_data, cleaning_frequency_int):
    call_data = call_data.split("$")
    call_data = call_data[1].split("*")
    room_amount = int(call_data[0])
    bathroom_amount = int(call_data[1])
    delta = date.today() + timedelta(days=1)
    delta = delta.strftime("%a:%d:%b")
    delta = delta.split(":")
    time_order = delta[0] + " " + delta[1] + " " + delta[2] + " 08:00"

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
            break

    standart_price = caption[standart_price_pos].split(" ")
    standart_price = int(standart_price[-1].replace('р', ""))

    old_time = caption[3]
    old_time = old_time.split(" ")
    hour = float(old_time[3])

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
                caption.pop(i)
                if extra_price != 0:
                    caption[-1] = "К оплате: " + str(extra_price) + "р"
                else:
                    caption[-1] = "К оплате: " + str(standart_price) + "р"
            if "Регулярность" in caption[i]:
                caption[i] = "Регулярность: " + "1 раз или первый раз"

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
            if "Регулярность" in caption[i]:
                caption[i] = "Регулярность: "
                # Сорри за костыль
                if discount_percent == 15:
                    caption[i] += "Раз в неделю"
                if discount_percent == 10:
                    caption[i] += "Раз в две недели"
                if discount_percent == 7:
                    caption[i] += "Раз в месяц"

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


def from_caption_to_dict(caption):
    caption = caption.split("\n")
    order_dict = empty_order
    pos = 0
    for i in range(len(caption)):
        if "Адрес" in caption[i]:
            pos = i
            break
        else:
            if "Уборка квартиры" in caption[i]:
                temp = caption[i].split(" ")
                order_dict["order_info"]["room"] = int(temp[3])
                order_dict["order_info"]["bathroom"] = int(temp[6])
                pass
            if "Дата уборки" in caption[i]:
                temp = caption[i].split(" ")
                order_dict["order_info"]["date"] = temp[2] + " " + temp[3] + " " + temp[4]
                order_dict["order_info"]["time"] = temp[5]
                pass
            if "Время уборки" in caption[i]:
                temp = caption[i].split(" ")
                order_dict["order_info"]["cleaning_time"] = float(temp[3])
                pass
            if "Регулярность" in caption[i]:
                temp = caption[i].split(":")
                order_dict["order_info"]["frequency"] = temp[1][1:]
                pass
            if "Стандарнатная стоимость" in caption[i]:
                temp = caption[i].split(" ")
                order_dict["order_info"]["standart_price"] = int(temp[2].replace("р",""))
                pass
            if "Дополнительные услуги" in caption[i]:
                for j in range(i+1,len(caption)-1):
                    if "Стоимость уборки с дополнительными" in caption[j]:
                        temp = caption[j].split(":")
                        order_dict["order_info"]["extra_price"] = int(temp[1][1:].replace("р", ""))
                        break
                    else:
                        for x in extra_name_hour_cost_dict.values():
                            if x[0] in caption[j]:
                                order_dict["order_info"]["extra_service"].append(x)
                                break
            if "Сумма скидки" in caption[i]:
                temp = caption[i].split(":")
                order_dict["order_info"]["discount_amount"] = float(temp[1][1:].replace("р", ""))
            if "К оплате" in caption[i]:
                temp = caption[i].split(":")
                order_dict["order_info"]["payment"] = float(temp[1][1:].replace("р", ""))

    for i in range(pos+1, len(caption)):
        if "Улица" in caption[i]:
            temp = caption[i].split(":")
            order_dict["address"]["street"] = temp[1][1:]
        if "Дом" in caption[i]:
            temp = caption[i].split(":")
            order_dict["address"]["house"] = temp[1][1:]
        if "Квартира" in caption[i]:
            temp = caption[i].split(":")
            order_dict["address"]["flat"] = temp[1][1:]
        if "ФИО" in caption[i]:
            temp = caption[i].split(":")
            order_dict["contact_info"]["name"] = temp[1][1:]
        if "Телефон" in caption[i]:
            temp = caption[i].split(":")
            order_dict["contact_info"]["tel"] = temp[1][1:]
        if "Email" in caption[i]:
            temp = caption[i].split(":")
            order_dict["contact_info"]["email"] = temp[1][1:]

    return order_dict


def is_admin(user_id):
    for x in admins:
        if int(user_id) == x:
            return True
    return False


def is_cleaner(user_id):
    for x in cleaners:
        if int(user_id) == x:
            return True
    return False


def get_text_from_order_dict(order_dict):
    text = ""
    ending_room = ""
    ending_bathroom = ""

    if order_dict["order_info"]["room"] <= 1:
        ending_room = "жилой"
    elif 1 < order_dict["order_info"]["room"]:
        ending_room = "жилыми"

    if order_dict["order_info"]["bathroom"] <= 1:
        ending_bathroom = "ванной"
    elif 1 < order_dict["order_info"]["bathroom"]:
        ending_bathroom = "ванными"

    text += "Уборка квартиры с " + str(order_dict["order_info"]["room"]) + " " + ending_room + " и " + str(order_dict["order_info"]["bathroom"]) + " " + ending_bathroom + " комнатами"
    text += "\n\nДата уборки: " + order_dict["order_info"]["date"] + " " + order_dict["order_info"]["time"]
    text += "\nВремя уборки: ~ " + str(order_dict["order_info"]["cleaning_time"]) + " ч."
    text += "\nРегулярность: " + order_dict["order_info"]["frequency"]
    text += "\nСтандарнатная стоимость: " + str(order_dict["order_info"]["standart_price"]) + "р"
    if len(order_dict["order_info"]["extra_service"]) != 0:
        text += "\nДополнительные услуги"
        for x in (order_dict["order_info"]["extra_service"]):
            text += "\n" + x[0] + ": " + str(x[2])
        text += "\nСтоимость уборки с дополнительными услугами: " + str(order_dict["order_info"]["extra_price"]) +"р"
    if order_dict["order_info"]["discount_amount"] is not None:
        text += "\nСумма скидки за регулярность: " + str(order_dict["order_info"]["discount_amount"]) + "р"
    text += "\nК оплате: " + str(order_dict["order_info"]["payment"]) + "р"

    text += "\n\nАдрес"
    text += "\nУлица: " + order_dict["address"]["street"]
    text += "\nДом: " + order_dict["address"]["house"]
    text += "\nКвартира: " + order_dict["address"]["flat"]

    text += "\n\nКонтактная информация"
    text += "\nФИО: " + order_dict["contact_info"]["name"]
    text += "\nТелефон: " + order_dict["contact_info"]["tel"]
    text += "\nEmail: " + order_dict["contact_info"]["email"]
    if order_dict["user_name"] is not None:
        text += "\n\nАккаунт @" + str(order_dict["user_name"])

    return text


def get_text_from_feedback_dict(feedback_number):
    feedback = feedbacks[feedback_number]
    text = ""
    text += feedback["name"]
    text += "\n" + feedback["text"]
    text += "\n\nУборка выполнена в " + feedback["date"]
    if feedback["cleaner"] != "company":
        text += "\nСпециалистом " + str(feedback["cleaner"])
    else:
        text +="\nКомпанией КлинниБогини"

    return text


def open_json_order_by_id(order_id):
    try:
        f = open("orders/" + str(order_id) + ".json", "r", encoding="utf-8")
        order_dict = json.loads(f.read())
        f.close()
    except:
        return ""
    return order_dict


def manual_assign_cleaner_to_order(cleaner_id, order_id):
    order_dict = {}
    temp = 0
    for x in not_verified_orders_list:
        if x[0] == order_id:
            order_dict = x[1]
            temp = 1
            break
    if temp == 0:
        return False, "Заказ не найден"
    date_cleaning = order_dict["order_info"]["date"]
    time_start = order_dict["order_info"]["time"]
    time_start = datetime.strptime(time_start, "%H:%M")
    time_cleaning = order_dict["order_info"]["cleaning_time"]
    street = order_dict["address"]["street"] + " " + order_dict["address"]["house"]
    time_end = time_start + timedelta(hours=time_cleaning)
    # 1ый этап - Проверка что время работы заказа меньше 9ч и что время окончания уборки не больше 22.00
    print("1-ый этап - проверка < 9 часов и до 22.00")
    if time_cleaning <= 9 and time_start + timedelta(hours=time_cleaning) <= datetime.strptime("22:00", "%H:%M"):
        print("1-ый этап пройден")
        # 2ой этап - Проверка Свободен ли этот день у клинера
        print("2-ой этап - Свободен ли у этого клинера день")
        if date_cleaning not in schedule[str(cleaner_id)].keys():
            print("2-ой этап пройден. День свободен")
            schedule[str(cleaner_id)][date_cleaning] = empty_day
            k = 0
            for i in range(len(schedule[str(cleaner_id)][date_cleaning])):
                if schedule[str(cleaner_id)][date_cleaning][i][0] == (time_start - timedelta(hours=1)).strftime("%H:%M") and k == 0:
                    schedule[str(cleaner_id)][date_cleaning][i].append("start")
                    schedule[str(cleaner_id)][date_cleaning][i].append(order_id)
                    schedule[str(cleaner_id)][date_cleaning][i].append(street)
                    schedule[str(cleaner_id)][date_cleaning][i][1] = False
                    k = 1
                    continue
                if k == 1 and schedule[str(cleaner_id)][date_cleaning][i][0] != time_end.strftime("%H:%M"):
                    schedule[str(cleaner_id)][date_cleaning][i][1] = False
                if k == 1 and schedule[str(cleaner_id)][date_cleaning][i][0] == time_end.strftime("%H:%M"):
                    schedule[str(cleaner_id)][date_cleaning][i-1].append("end")
                    break
            set_schedule_to_json(schedule)
            return True, "Успешно назначили клинера " + str(cleaner_id)
        else:
            print("2-этап не пройден. День занят. Проверка есть ли свободное место в этом дне")
            # 2ой этап - Если в этот день у клинера уже есть заказ - Проверяем, свободен ли промежуток времени для данной уборки
            for i in range(len(schedule[str(cleaner_id)][date_cleaning])):
                if schedule[str(cleaner_id)][date_cleaning][i][0] == (time_start - timedelta(hours=1)).strftime("%H:%M"):
                    print("Нашло время начала уборки и время в расписании")
                    if schedule[str(cleaner_id)][date_cleaning][i][1] == False:
                        print("Начало уборки занято - выход из функции")
                        return False, "На это время этот клинер " + str(cleaner_id) + " занят. Попробуйте другого"
                    else:
                        for j in range(i+1, len(schedule[str(cleaner_id)][date_cleaning])):
                            if schedule[str(cleaner_id)][date_cleaning][j][0] == time_end.strftime("%H:%M"):
                                print("остановили поиск свободного времени. Дошли до времени окончания")
                                break
                            if schedule[str(cleaner_id)][date_cleaning][j][1] == False:

                                return False, "На это время этот клинер " + str(cleaner_id) + " занят. Попробуйте другого"
                        print("Время свободно. Заполняем время")
                        k = 0
                        for i in range(len(schedule[str(cleaner_id)][date_cleaning])):
                            if schedule[str(cleaner_id)][date_cleaning][i][0] == (time_start - timedelta(hours=1)).strftime("%H:%M") and k == 0:
                                print("Время старта совпало с ячейкой времени. Заполняем start order_id street и ячейку false")
                                schedule[str(cleaner_id)][date_cleaning][i].append("start")
                                schedule[str(cleaner_id)][date_cleaning][i].append(order_id)
                                schedule[str(cleaner_id)][date_cleaning][i].append(street)
                                schedule[str(cleaner_id)][date_cleaning][i][1] = False
                                k = 1
                                continue
                            if k == 1 and schedule[str(cleaner_id)][date_cleaning][i][0] != time_end.strftime("%H:%M"):
                                print("заполняем ячейку", schedule[str(cleaner_id)][date_cleaning][i][0])
                                schedule[str(cleaner_id)][date_cleaning][i][1] = False
                                # schedule[str(cleaner_id)][date_cleaning][i].append("")
                                # schedule[str(cleaner_id)][date_cleaning][i].append(order_id)
                            if k == 1 and schedule[str(cleaner_id)][date_cleaning][i][0] == time_end.strftime("%H:%M"):
                                print("Поймали последнюю ячейку", schedule[str(cleaner_id)][date_cleaning][i][0])
                                print("дописываем в предыдущую ячейку - false", schedule[str(cleaner_id)][date_cleaning][i -1])
                                (schedule[str(cleaner_id)][date_cleaning][i - 1]).append("end")
                                break
                        set_schedule_to_json(schedule)
                        return True, "Успешно Назначили клинера " + str(cleaner_id)
    else:
        print("1-ый этап не пройден")
        return False, "Тут Хуета\nЛибо заказ длится больше 9 часов\nЛибо он закончится позже 22:00\nА в  ручную  пока что двоих клинеров нельзя назначить :("




