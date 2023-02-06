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
