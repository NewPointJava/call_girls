from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import extra_name_hour_cost_dict, feedbacks, cleaners

exit_button = InlineKeyboardButton("Выход ❌", callback_data="qt")
thanks_buttom = InlineKeyboardButton("Cпасибо ☑", callback_data="qt")
thanks_keyboard = InlineKeyboardMarkup().add(thanks_buttom)



def price_1st_step(room_amount, bathroom_amount):
    keyboard = InlineKeyboardMarkup(row_width=2)

    increase_room = InlineKeyboardButton("кол-во комнат ➕", callback_data="st1*" + str(room_amount + 1) + "*" + str(bathroom_amount))
    decrease_room = InlineKeyboardButton("кол-во комнат ➖", callback_data="st1*" + str(room_amount - 1) + "*" + str(bathroom_amount))
    increase_bathroom = InlineKeyboardButton("кол-во санузлов ➕", callback_data="st1*" + str(room_amount) + "*" + str((bathroom_amount +1)))
    decrease_bathroom = InlineKeyboardButton("кол-во санузлов ➖", callback_data="st1*" + str(room_amount) + "*" + str((bathroom_amount-1)))
    second_step_bottom = InlineKeyboardButton("Рассчитать стоимость ☑️", callback_data="st1$" + str(room_amount) + "*" + str(bathroom_amount))

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
    keyboard.add(exit_button)

    return keyboard


def st2_keyboard(room_amount, bathroom_amount):
    keyboard = InlineKeyboardMarkup()
    choose_date_bottom = InlineKeyboardButton("Выбрать дату уборки 🗓", callback_data="st2*date")
    return_bottom = InlineKeyboardButton("Вернуться назад к выбору количества комнат 🔙", callback_data="st1:"+str(room_amount) + "*" + str(bathroom_amount))
    keyboard.add(choose_date_bottom)
    keyboard.add(return_bottom)
    keyboard.add(exit_button)
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


def st2_extra_service_keyboard(room_amount, bathroom_amount):
    keyboard = InlineKeyboardMarkup()

    choose_extra_service_bottom = InlineKeyboardButton("Выбрать дополнительные опции ☑️", callback_data="st2*extra")
    return_bottom = InlineKeyboardButton("Вернуться на шаг назад 🔙", callback_data="st1$"+ str(room_amount) + "*" + str(bathroom_amount))

    keyboard.add(choose_extra_service_bottom)
    keyboard.add(return_bottom)
    keyboard.add(exit_button)

    return keyboard

def extra_service_st1_keyboard(caption):
    print("extra_service_st1_keyboard")
    caption = caption.split("\n")
    keyboard = InlineKeyboardMarkup(row_width=3)
    next_bottom = InlineKeyboardButton("Перейти к следующему шагу ☑️", callback_data="st2*frequency")
    temp = 0

    for k in extra_name_hour_cost_dict.keys():
        buf = 0
        for i in range(len(caption)):
            if i != len(caption)-1:
                if extra_name_hour_cost_dict[k][0] in caption[i]:
                    buf += 1
            else:
                if buf > 0:
                    keyboard.add(InlineKeyboardButton(extra_name_hour_cost_dict[k][0] + " ➖", callback_data="st2*en$" + k + "-"))
                else:
                    keyboard.add(InlineKeyboardButton(extra_name_hour_cost_dict[k][0] + " ➕", callback_data="st2*en$" + k + "+"))

    keyboard.add(next_bottom)

    return keyboard


def st2_frequency_keyboard(caption):
    caption = caption.split("\n")
    for x in caption:
        if "Дата уборки:" in x:
            time = x
            time = time.split(" ")
            time = time[-1]
            print(time)

    keyboard = InlineKeyboardMarkup()
    choose_frequency_bottom = InlineKeyboardButton("Выбрать частоту уборки ☑️", callback_data="st2*fn")
    return_bottom = InlineKeyboardButton("Вернуться на шаг назад 🔙", callback_data="st2*time$" + time)

    keyboard.add(choose_frequency_bottom)
    keyboard.add(return_bottom)
    keyboard.add(exit_button)

    return keyboard


def choose_frequency_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    frequency_weekly_bottom = InlineKeyboardButton("Раз в неделю - Скидка  15%", callback_data="st2*ff%15")
    frequency_2time_in_week_bottom = InlineKeyboardButton("Раз в две недели - Скидка  10%", callback_data="st2*ff%10")
    frequency_monthly_bottom = InlineKeyboardButton("Раз в месяц - Скидка  7%", callback_data="st2*ff%7")
    frequency_one_time_bottom = InlineKeyboardButton("1 раз или первый раз", callback_data="st2*ff%0")
    return_bottom = InlineKeyboardButton("Вернуться на шаг назад 🔙", callback_data="st2*frequency")
    next_bottom = InlineKeyboardButton("Перейти к проверке заказа ☑️", callback_data="st2*check_order")

    keyboard.add(frequency_weekly_bottom, frequency_2time_in_week_bottom, frequency_monthly_bottom, frequency_one_time_bottom)
    keyboard.add(next_bottom)
    keyboard.add(return_bottom)
    keyboard.add(exit_button)

    return keyboard


def check_order_keyboard(caption):

    keyboard = InlineKeyboardMarkup(row_width=1)

    return_to_date = InlineKeyboardButton("Изменить Дату и Время заказа 🗓", callback_data="st2*date" )
    return_to_extra_service = InlineKeyboardButton("Изменить дополнительные услуги", callback_data="st2*extra")
    return_to_frequency = InlineKeyboardButton("Изменить регулярность уборки", callback_data="st2*fn")
    save_bottom = InlineKeyboardButton("Перейти к заполнению адреса ☑", callback_data="st3*address")


    keyboard.add(return_to_date,return_to_extra_service,return_to_frequency,save_bottom,exit_button)

    return keyboard


def send_order_to_admin():
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton("Заказать уборку ☑️", callback_data="add"), InlineKeyboardButton("Удалить заказ",callback_data="qt"))
    return keyboard


def not_verified_slider_keyboard(not_verified_orders_list, page_number):
    keyboard = InlineKeyboardMarkup(row_width=3)

    backbutton = InlineKeyboardButton(text="предыдущие", callback_data="nt_ver*" + str(page_number - 1))
    nextbutton = InlineKeyboardButton(text="следующие", callback_data="nt_ver*" + str(page_number + 1))
    exitbutton = InlineKeyboardButton(text="выход", callback_data="qt")
    if len(not_verified_orders_list) != 0 :
        if len(not_verified_orders_list) < 10:
            button_list = [InlineKeyboardButton(text=x[1]["order_info"]["date"], callback_data="nt_ver:" + str(x[0])) for x in
                           not_verified_orders_list]
            keyboard.add(*button_list)
        elif 9 * (page_number + 1) < len(not_verified_orders_list) and 9 * page_number <= 0:
            button_list = [InlineKeyboardButton(text=x[1]["order_info"]["date"], callback_data="nt_ver:" + str(x[0])) for x in
                           not_verified_orders_list[page_number * 9:(page_number + 1) * 9]]
            keyboard.add(*button_list)
            keyboard.add(nextbutton)
        elif 9 * (page_number + 1) >= len(not_verified_orders_list):
            button_list = [InlineKeyboardButton(text=x[1]["order_info"]["date"], callback_data="nt_ver:" + str(x[0])) for x in
                           not_verified_orders_list[page_number * 9:(page_number + 1) * 9]]
            keyboard.add(*button_list)
            keyboard.add(backbutton)
        else:
            button_list = [InlineKeyboardButton(text=x[1]["order_info"]["date"], callback_data="nt_ver:" + str(x[0])) for x in
                           not_verified_orders_list[page_number * 9:(page_number + 1) * 9]]
            keyboard.add(*button_list)
            keyboard.add(backbutton, nextbutton)

    keyboard.add(exitbutton)
    return keyboard


def admin_check_order_keyboard(order_id):

    keyboard = InlineKeyboardMarkup(row_width=1)

    avto_search_bottom = InlineKeyboardButton("Автоматический поиск клинера 🤖", callback_data="av_sh:" + str(order_id))
    manual_search_bottom = InlineKeyboardButton("Ручной поиск клинера 🕹", callback_data="ml_sh:" + str(order_id))
    del_order_bottom = InlineKeyboardButton("Удалить заказ ⛔️", callback_data="nt_ver-" + str(order_id))
    return_bottom = InlineKeyboardButton("Вернуться назад к списку 🔙", callback_data="ntvr")
    save_bottom = InlineKeyboardButton("Сохранить Test", callback_data="save*" + str(order_id))

    keyboard.add(avto_search_bottom, manual_search_bottom, del_order_bottom, return_bottom, exit_button, save_bottom)

    return keyboard


def feedbacks_slider_keyboard(feedback_number):

    keyboard = InlineKeyboardMarkup(row_width=3)
    next_number = feedback_number+1
    back_number = feedback_number-1

    if back_number == -1:
        back_number = len(feedbacks)-1
    if next_number == len(feedbacks):
        next_number = 0

    next_bottom = InlineKeyboardButton("Следующий ➡️", callback_data="fb*" + str(next_number))
    back_bottom = InlineKeyboardButton("⬅️Предыдущий", callback_data="fb*" + str(back_number))

    if len(feedbacks) <=1:
        keyboard.add(exit_button)
    else:
        keyboard.add(back_bottom, exit_button, next_bottom)

    return keyboard


def choose_cleaner_keyboard(order_id):
    keyboard = InlineKeyboardMarkup()
    button_list = [InlineKeyboardButton(text=str(x), callback_data="cl:"+ str(x) + "*" + str(order_id))for x in cleaners]
    back_bottom = InlineKeyboardButton("Вернуться назад 🔙", callback_data="nt_ver:" + str(order_id))

    keyboard.add(*button_list)
    keyboard.add(back_bottom)
    keyboard.add(exit_button)

    return keyboard