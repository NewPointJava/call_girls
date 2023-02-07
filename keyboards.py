from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def price_1st_step(room_amount, bathroom_amount):
    keyboard = InlineKeyboardMarkup(row_width=2)
    # if room_amount == 0:
    #     room_amount = 1
    # if room_amount == 11:
    #     room_amount = 10
    #
    # if bathroom_amount == 0:
    #     bathroom_amount = 1
    # if bathroom_amount == 11:
    #     bathroom_amount = 10


    increase_room = InlineKeyboardButton("увеличить кол-во комнат", callback_data="st1*" + str(room_amount + 1) + "*" + str(bathroom_amount))
    decrease_room = InlineKeyboardButton("уменьшить кол-во комнат", callback_data="st1*" + str(room_amount - 1) + "*" + str(bathroom_amount))
    increase_bathroom = InlineKeyboardButton("увеличить кол-во санузлов", callback_data="st1*" + str(room_amount) + "*" + str((bathroom_amount +1)))
    decrease_bathroom = InlineKeyboardButton("уменьшить кол-во санузлов", callback_data="st1*" + str(room_amount) + "*" + str((bathroom_amount-1)))
    second_step_bottom = InlineKeyboardButton("Рассчитать стоимость", callback_data="st1$" + str(room_amount) + "*" + str(bathroom_amount))
    exitbutton = InlineKeyboardButton(text="Выход", callback_data="qt")

    if room_amount != 1 and room_amount != 10:
        keyboard.add(increase_room, decrease_room)
    elif room_amount == 1:
        keyboard.add(increase_room)
    elif room_amount == 10:
        keyboard.add(decrease_room)

    if bathroom_amount != 1 and bathroom_amount != 10:
        keyboard.add(increase_bathroom, decrease_bathroom)
    elif bathroom_amount == 1:
        keyboard.add(increase_bathroom)
    elif bathroom_amount == 10:
        keyboard.add(decrease_bathroom)

    keyboard.add(second_step_bottom)
    keyboard.add(exitbutton)

    return keyboard


def st2_keyboard(room_amount, bathroom_amount):
    keyboard = InlineKeyboardMarkup()
    choose_date_bottom = InlineKeyboardButton("Выбрать дату уборки", callback_data="st2*date")
    choose_frequency_bottom = InlineKeyboardButton("Выбрать регулярность уборки", callback_data="st2*frequency")
    return_bottom = InlineKeyboardButton("Вернуться назад к выбору количества комнат",callback_data="st1:"+str(room_amount) + "*" + str(bathroom_amount))
    exitbutton = InlineKeyboardButton("Выход", callback_data="qt")
    keyboard.add(choose_date_bottom)
    keyboard.add(choose_frequency_bottom)
    keyboard.add(return_bottom)
    keyboard.add(exitbutton)
    return keyboard

def choose_time_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=5)
    hour = 9
    bottom_name_list = []
    for i in range(19):
        if i %2 ==0:
            bottom_name_list.append(str(hour)+":00")
        else:
            bottom_name_list.append(str(hour)+":30")
            hour+=1

    button_list = [InlineKeyboardButton(text=x, callback_data="st2*time$"+x) for x in bottom_name_list]
    keyboard.add(*button_list)

    return keyboard

def choose_frequency_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    frequency_weekly_bottom = InlineKeyboardButton("Раз в неделю - Скидка = 15%", callback_data="st2*fr%15")
    frequency_2time_in_week_bottom = InlineKeyboardButton("Раз в две недели - Скидка = 10%", callback_data="st2*fr%10")
    frequency_monthly_bottom = InlineKeyboardButton("Раз в месяц - Скидка = 7%", callback_data="st2*fr%7")
    frequency_one_time_bottom = InlineKeyboardButton("1 раз или первый раз", callback_data="st2*fr%0")

    keyboard.add(frequency_weekly_bottom,frequency_2time_in_week_bottom,frequency_monthly_bottom,frequency_one_time_bottom)

    return keyboard
