from settings import check_in_price, room_price, bathroom_price, check_in_time, room_time, bathroom_time, cleaning_frequency_dict


def cost_calculation_st1(call_data):
    call_data = call_data.split("*")
    room_amount = int(call_data[1])
    bathroom_amount = int(call_data[2])

    print(f'room ={room_amount}, bathromm ={bathroom_amount}')
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
    print(time_order)
    time_order = time_order[0] + " " + time_order[1] + " " + str(int(time_order[3]) + 1) + " 09:00"
    print(time_order)

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

    cleaning_frequency = cleaning_frequency_dict[str(cleaning_frequency_int)]
    discount = cleaning_frequency[1]
    cleaning_frequency = cleaning_frequency[0]
    print(cleaning_frequency, discount)

    text = f'Уборка квартиры с {room_amount} {ending_room} и  {bathroom_amount} {ending_bathroom} комнатами\n\n'\
            f'Дата уборки: {time_order}\n'\
            f'Время уборки: ~ {cleaning_time} ч.\n'\
            f'Регулярность: {cleaning_frequency}\n\n'\
            f'Стандарнатная стоимость: {check_in_price + room_amount * room_price + bathroom_amount * bathroom_price}'

    return text
