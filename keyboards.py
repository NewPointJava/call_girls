from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import extra_name_hour_cost_dict, feedbacks, cleaners, schedule


exit_button = InlineKeyboardButton("Выход ❌", callback_data="qt")
exit_keyboard = InlineKeyboardMarkup().add(exit_button)
thanks_buttom = InlineKeyboardButton("Cпасибо ☑", callback_data="qt")
thanks_keyboard = InlineKeyboardMarkup().add(thanks_buttom)

successful_cleaner_assign_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Вернуться к списку заказов", callback_data="ntvr")).add(exit_button)


def price_1st_step_keyboard(room_amount, bathroom_amount):
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


def check_order_keyboard():

    keyboard = InlineKeyboardMarkup(row_width=1)

    return_to_date = InlineKeyboardButton("Изменить Дату и Время заказа 🗓", callback_data="st2*date" )
    return_to_extra_service = InlineKeyboardButton("Изменить дополнительные услуги", callback_data="st2*extra")
    return_to_frequency = InlineKeyboardButton("Изменить регулярность уборки", callback_data="st2*fn")
    save_bottom = InlineKeyboardButton("Перейти к заполнению адреса ☑", callback_data="st3*address")


    keyboard.add(return_to_date,return_to_extra_service,return_to_frequency,save_bottom,exit_button)

    return keyboard


def send_order_to_admin_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Заказать уборку ☑️", callback_data="add"), InlineKeyboardButton("Удалить заказ",callback_data="qt"))
    return keyboard


def not_verified_slider_keyboard(not_verified_orders_list, page_number):
    # Создаёт клавиатуру слайдер для просмотра всех необрабработанных заказов

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
    # Клавиатура для преключения между отзывами

    keyboard = InlineKeyboardMarkup(row_width=3)
    next_number = feedback_number+1
    back_number = feedback_number-1

    if back_number == -1:
        back_number = len(feedbacks)-1
    if next_number == len(feedbacks):
        next_number = 0

    next_bottom = InlineKeyboardButton("Следующий ➡️", callback_data="fb*" + str(next_number))
    back_bottom = InlineKeyboardButton("⬅️ Предыдущий", callback_data="fb*" + str(back_number))

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


def view_new_order_keyboard(order_id):
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Просмотреть заказ", callback_data="nt_ver:" + str(order_id))).add(exit_button)
    return keyboard


def schedule_slider_keyboard(cleaner_id, page_number):
    cleaner_schedule = schedule[str(cleaner_id)]
    work_days = sorted(cleaner_schedule)
    today = datetime.now()
    all_days = []
    for i in range(60):
        all_days.append(today.strftime("%a %d %b"))
        today = today + timedelta(days=1)

    day_week = (datetime.now()).strftime("%a")
    if day_week != "Пн":
        for i in range(7):
            if (datetime.now() - timedelta(days=i+1)).strftime("%a") == "Пн":
                all_days.insert(0, (datetime.now() - timedelta(days=i + 1)).strftime("%a %d %b"))
                break
            else:
                all_days.insert(0, (datetime.now() - timedelta(days=i+1)).strftime("%a %d %b"))

    for i in range(7):
            all_days.insert(0, (datetime.now() - timedelta(days=i + 1)).strftime("%a %d %b"))

    keyboard = InlineKeyboardMarkup(row_width=3)

    backbutton = InlineKeyboardButton(text="⬅", callback_data="schedule*" + str(page_number - 1))
    nextbutton = InlineKeyboardButton(text="️➡", callback_data="schedule*" + str(page_number + 1))

    slice_start = page_number*7
    slice_end = (page_number+1)*7
    if slice_end > len(all_days):
        slice_end = len(all_days)
    for x in all_days[slice_start:slice_end]:
        k = 0
        for wd in work_days:
            if wd.casefold() == x.casefold():
                k = 1
        if k == 1:
            keyboard.add(InlineKeyboardButton(x + " 🔴", callback_data="scwd*" + str(x) + ":" + str(page_number)))
        else:
            keyboard.add(InlineKeyboardButton(x + " ⚪️", callback_data="day_off*" + str(page_number)))
    if page_number == 0:
        keyboard.add(exit_button,nextbutton)
    elif slice_end == len(all_days):
        keyboard.add(backbutton, exit_button)
    else:
        keyboard.add(backbutton, exit_button, nextbutton)

    return keyboard

def schedule_view_work_day(cleaner_id, work_day, return_page_number):
    cleaner_work_day = schedule[str(cleaner_id)][work_day]
    order_list = []
    time_start_list = []
    time_end_list = []
    address_list = []
    temp = 0
    for x in cleaner_work_day:
        if len(x) == 5:
            order_list.append(x[3])
            time_start_list.append(x[0])
            address_list.append(x[4])
        elif len(x) == 3:
                time_end_list.append(x[0])
    keyboard = InlineKeyboardMarkup(row_width=1)

    for i in range(len(order_list)):
        time_start_list[i] = (datetime.strptime(time_start_list[i], "%H:%M") + timedelta(hours=1)).strftime("%H:%M")
        time_end_list[i] = (datetime.strptime(time_end_list[i], "%H:%M") + timedelta(minutes=30)).strftime("%H:%M")

    bottom_list = [InlineKeyboardButton("🕐" +time_start_list[i] + " - " + time_end_list[i] + ", 🏠 " + address_list[i], callback_data="sc_order*" + str(order_list[i]) + ":" + work_day + ":" + return_page_number) for i in range(len(order_list))]
    return_bottom = InlineKeyboardButton("🔙 Вернуться к выбору дня ", callback_data="sc_return*" + return_page_number)
    keyboard.add(*bottom_list, return_bottom, exit_button)

    return keyboard


def cleaner_view_order_keyboard(order_id, return_work_day, return_number_page, order_dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    return_to_choose_order_bottom = InlineKeyboardButton("🔙  Вернуться к выбору заказа", callback_data="scwd*" + return_work_day+":" + str(return_number_page))
    return_to_choose_work_day_bottom = InlineKeyboardButton("🔙  Вернуться к выбору рабочего дня", callback_data="sc_return*" + str(return_number_page))
    done_cleaning_bottom = InlineKeyboardButton("✅ Уборка закончена\nОтправить запрос на отзыв", callback_data="done*"+ str(order_id))
    today = datetime.now()
    date_start = datetime.strptime(str(today.year) + " " + order_dict["order_info"]["date"] + " " + order_dict["order_info"]["time"], "%Y %a %d %b %H:%M")
    customer_id = order_dict["user_id"]

    keyboard.add(return_to_choose_order_bottom, return_to_choose_work_day_bottom)
    if date_start < today:
        keyboard.add(done_cleaning_bottom)
    keyboard.add(exit_button)
    return keyboard


def ask_to_feedback_keyboard(order_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Оставить отзыв", callback_data="cutomer_fb*" + str(order_id)))
    keyboard.add(thanks_buttom)
    return keyboard


def accept_feedback_keyboard(order_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Сохранить отзыв", callback_data="accept_fb*" + str(order_id)))
    keyboard.add(exit_button)
    return keyboard
