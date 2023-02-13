import json
from datetime import date, timedelta
from telegram_bot_calendar import DetailedTelegramCalendar
from keyboards import price_1st_step_keyboard, st2_keyboard, choose_time_keyboard, choose_frequency_keyboard, \
    st2_frequency_keyboard, extra_service_st1_keyboard, st2_extra_service_keyboard, check_order_keyboard, \
    thanks_keyboard, not_verified_slider_keyboard, admin_check_order_keyboard, feedbacks_slider_keyboard, \
    choose_cleaner_keyboard, successful_cleaner_assign_keyboard, view_new_order_keyboard, schedule_slider_keyboard, \
    schedule_view_work_day, cleaner_view_order_keyboard, exit_keyboard, ask_to_feedback_keyboard
from next_step_handlers_func import cath_addres, cath_feed_back
from service_function import cost_calculation_st1, order_card, edit_order_caption_date, edit_order_caption_time, \
    edit_caption_extra_service, edit_caption_discount, from_caption_to_dict, is_admin, \
    get_text_from_order_dict, get_text_from_feedback_dict, is_cleaner, manual_assign_cleaner_to_order, save_feedback
from get_and_set_json_information import get_and_set_order_id_from_json, get_order_dict_from_json_by_id, \
    update_order_json_from_dict
from settings import bot, room_price, bathroom_price, check_in_price, orders, not_verified_orders_list, admins


@bot.message_handler(commands=['start'])
def start(message):
    text ="""Вас приветсвует компания КлинниБогини!
Этот чат-бот поможет вам заказать уборку быстро и без лишних разговоров

/new_order - Нажмите чтобы начать оформление заказа

/view_feedbacks - Нажмите чтобы посмотреть отзывы о компании

/help - Нажмите чтобы получить больше информацией по управлению ботом

/info - Нажмите чтобы узнать подробнее о компании
"""
    bot.send_message(message.chat.id, text, reply_markup=thanks_keyboard)


@bot.message_handler(commands=['help'])
def help_user(message):
    text = f'ПОЛЬЗОВАТЕЛЯМ\n'\
            f'Этот бот создан чтобы помочь вам сделать заказ на уборку в клининговой компании КлинниБогини\n'\
            f'Для создания заказа используйте команду /new_order\n\n'\
            f'Так же вы можете просмотреть отзывы о нашей компании\n'\
            f'Для просмотра отзывов используйте команду /view_feedbacks\n\n'\
            f'Чтобы получить больше информации о компании используйте команду /info\n\n\n'\
            f'КЛИНЕРАМ\n'\
            f'Чтобы получить доп информацию о возможностях бота\n'\
            f'Используйте команду /cl_help\n\n\n'\
            f'АДМИНИСТРАТОРАМ\n'\
            f'Чтобы получить доп информацию о возможностях бота\n'\
            f'Используйте команду /ad_help'

    bot.send_message(message.chat.id, text, reply_markup=thanks_keyboard)


@bot.message_handler(commands=['info'])
def info(message):
    text = f'КлинниБогини - Уборка квартир и домов в Минске и районе, хорошо или бесплатно\n'\
        f' +375447111185 (A1,Viber,Telegram,Whatsapp)\n\n'\
        f'Режим работы\n'\
        f'с 9.00 до 21.00 - без выходных\n\n'\
        f'Наш сайт\n'\
        f'cleanny.by\n\n'\
        f'Блог КлинниБогини\n'\
        f'cleanny.by/blog\n\n'\
        f'Отзывы\n'\
        f'/view_feedbacks\n'\
        f'а так же на FB - www.facebook.com/pg/cleanny.happy.home/reviews/\n\n'\
        f'Чек-лист уборки - https://drive.google.com/file/d/1gH8ogErgeWSeqIPhM9XQVPitbmzHxG1v/view\n\n'\
        f'Сделать заказ - /new_order\n\n'\
        f'© 2022 ООО «Клинни Про», УНП 192598987 Республика Беларусь, 220036, Минск, ул. Западная 13, часть комнаты 10-Ф'
    bot.send_message(message.chat.id, text, reply_markup=thanks_keyboard)


@bot.message_handler(commands=['ad_help'])
def ad_help(message):
    text = """/new_order - Нажми чтобы создать заказ.
После ввода всей информации, заказ сохранится в необработанных и вам предложат выбор :
Назначить клинера ручным или автоматическим способом, либо же удалить заказ. 

/not_verified - Показывает список всех необработанных заказов.
Нажмите на дату заказа и обработайте его.
"""
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, text, reply_markup=thanks_keyboard)
    else:
        bot.send_message(message.chat.id, "‼ Вы не обладаете правами доступа ‼", reply_markup=exit_keyboard)


@bot.message_handler(commands=['cl_help'])
def cl_help(message):
    text = """/schedule - Просмотреть расписание.
Символы помогают увидеть дни
🔴 - когда есть заказы ⚪️ - когда нет заказов

Нажмите на день недели, чтобы увидеть заказы.

На следующем этапе нажмите на заказ - чтобы увидеть его подробности.
Кроме того на этапе просмотра заказа если вы выполнили заказ, у вас появиться кнопка - 

✅ Уборка закончена. Отправить запрос на отзыв

Нажав на неё заказчику придёт уведомление о завершении уборки, а так же запрос на оставление отзыва.
"""
    if is_cleaner(message.chat.id):
        bot.send_message(message.chat.id, text, reply_markup=thanks_keyboard)
    else:
        bot.send_message(message.chat.id, "‼ Вы не обладаете правами доступа ‼", reply_markup=exit_keyboard)

@bot.message_handler(commands=['new_order'])
def new_order(message):
    bot.send_message(message.chat.id, "Ниже будет представлен расчёт стоимости.\nВы можете увеличивать и уменьшать количество комнат и санузлов.\n "\
            "Далее вы сможете изменять время, частоту и доп. услуги.\n\nСтоимость будет меняться автоматически", reply_markup=thanks_keyboard)
    bot.send_message(message.chat.id, f'1 - комната 1 - санузел = {room_price + bathroom_price + check_in_price}р', reply_markup=price_1st_step_keyboard(1, 1))


@bot.message_handler(commands=['not_verified'])
def not_verified(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Вот список не проверенных заказов", reply_markup=not_verified_slider_keyboard(not_verified_orders_list, 0))
    else:
        bot.send_message(message.chat.id, "‼ Вы не обладаете правами доступа ‼", reply_markup=exit_keyboard)


@bot.message_handler(commands=['view_feedbacks'])
def view_feedback(message):
    text = get_text_from_feedback_dict(0)
    bot.send_message(message.chat.id, text, reply_markup=feedbacks_slider_keyboard(0))


@bot.message_handler(commands=['schedule'])
def view_schedule(message):
    if is_cleaner(message.chat.id):
        bot.send_message(message.chat.id, "Выберите день недели\n🔴 - есть заказы\n⚪ - нет заказов", reply_markup=schedule_slider_keyboard(message.chat.id, 1))
    elif is_admin(message.chat.id):
        bot.send_message(message.chat.id, "На данном этапе реализовано только для клинеров\nДобавьте свой id в list клеанеров\n(в jsons_config/settings.json  key = 'cleaners')")
    else:
        bot.send_message(message.chat.id, "Вы не являетесь клиннером компании", reply_markup=thanks_keyboard)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(call):
    result, key, step = DetailedTelegramCalendar(min_date=(date.today() + timedelta(days=1)), max_date=date.today()+timedelta(days=60)).process(call.data)
    if not result and key:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,reply_markup=key)
    elif result:
        bot.edit_message_caption(edit_order_caption_date(call.message.caption, result), call.message.chat.id, call.message.message_id, reply_markup=choose_time_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def call(call):
    print("call data = ", call.data)
    if call.data[:2] == "qt":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data[:3] == "st1":
        if call.data[3] != "$":
            if call.data[3] != ":":
                new_text, room_amount, bathroom_amount = cost_calculation_st1(call.data)
                bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id, reply_markup=price_1st_step_keyboard(room_amount, bathroom_amount))
            else:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                amount = call.data.split(":")
                amount = amount[1].split("*")
                amount[0] = int(amount[0])
                amount[1] = int(amount[1])
                bot.send_message(call.message.chat.id,
                                 f'{amount[0]} - комната {amount[1]} - санузел = {check_in_price + room_price*amount[0] + bathroom_price* amount[1]}р',
                                 reply_markup=price_1st_step_keyboard(int(amount[0]), int(amount[1])))

        if call.data[3] =="$":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            caption, room_amount, bathroom_amount = order_card(call.data, 4)
            bot.send_photo(call.message.chat.id, "https://kartinkin.net/uploads/posts/2021-07/1626169458_2-kartinkin-com-p-uborka-art-art-krasivo-3.jpg", caption, reply_markup=st2_keyboard(room_amount,bathroom_amount))

    if call.data[:3] == "st2":
        if call.data[4:] == "date":
            calendar, step = DetailedTelegramCalendar(min_date=(date.today() + timedelta(days=1)), max_date=date.today()+timedelta(days=60)).build()
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=calendar)

        if call.data[4:8] == "time":
            cleaning_time = call.data.split("$")
            cleaning_time = cleaning_time[1]
            caption, room_amount, bathroom_amount = edit_order_caption_time(call.message.caption, cleaning_time)
            try:
                bot.edit_message_caption(caption, call.message.chat.id, call.message.message_id, reply_markup=st2_extra_service_keyboard(room_amount, bathroom_amount))
            except:
                bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id, reply_markup=st2_extra_service_keyboard(room_amount, bathroom_amount))

        if call.data[4:] == "extra":
            bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id, reply_markup=extra_service_st1_keyboard(call.message.caption))

        if call.data[4:6] == "en":
            caption = edit_caption_extra_service(call.message.caption, call.data)
            bot.edit_message_caption(caption, call.message.chat.id, call.message.message_id, reply_markup=extra_service_st1_keyboard(caption))


        if call.data[4:] == "frequency":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=st2_frequency_keyboard(call.message.caption))

        if call.data[4:6] == "fn":
            bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id, reply_markup=choose_frequency_keyboard())

        if call.data[4:6] == "ff":
            discount = call.data.split("%")
            discount = discount[-1]
            caption = edit_caption_discount(call.message.caption, discount)
            try:
                bot.edit_message_caption(caption, call.message.chat.id, call.message.message_id, reply_markup=choose_frequency_keyboard())
            except:
                bot.answer_callback_query(call.id, "Этот параметр уже установлен", show_alert=False)
        if call.data[4:] == "check_order":
            bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,reply_markup=check_order_keyboard())

    if call.data[:3] == "st3":
        if call.data[4:] == "address":
            order_id = call.message.message_id
            orders[call.message.chat.id] = call.message.caption
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            text = 'Улица:\nДом:\nКвартира:\n\nОтправьте сообщением название улицы ⬇️'
            m = bot.send_message(call.message.chat.id, text)
            m_id = m.message_id
            bot.register_next_step_handler(m, cath_addres, text, m_id, order_id)

    if call.data == "add":
        order_id = get_and_set_order_id_from_json()
        order_dict = from_caption_to_dict(call.message.caption)
        order_dict["user_id"] = call.message.chat.id
        order_dict["user_name"] = call.from_user.username
        not_verified_orders_list.append([order_id, order_dict])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Заказ Сформирован\nID заказа - " + str(order_id) +"\n После проверки заказа и назначения клинeра, вам придёт уведомление")
        try:
            for x in admins:
                bot.send_message(x, "Поступил новый заказ. ID - " + str(order_id), reply_markup=view_new_order_keyboard(order_id))
        except:
            print("Сформирован заказ - ID = " + order_id + "\n", order_dict)

    if call.data == "ntvr":
        bot.delete_message(call.message.chat.id,call.message.message_id)
        bot.send_message(call.message.chat.id, "Вот список не проверенных заказов", reply_markup=not_verified_slider_keyboard(not_verified_orders_list, 0))

    if call.data[:6] == "nt_ver":
        if call.data[6] == "*":
            number_page = call.data.split("*")
            number_page = int(number_page[1])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup= not_verified_slider_keyboard(not_verified_orders_list, number_page))

        elif call.data[6] == ":":
            order_id = call.data.split(":")
            order_id = int(order_id[1])
            for x in not_verified_orders_list:
                if x[0] == order_id:
                    text = get_text_from_order_dict(x[1])
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, "https://i.artfile.ru/1920x1200_645851_[www.ArtFile.ru].jpg", text, reply_markup= admin_check_order_keyboard(order_id))

        elif call.data[6] == "-":
            order_id = call.data.split("-")
            order_id = int(order_id[1])
            bot.delete_message(call.message.chat.id, call.message.message_id)
            for i in range(len(not_verified_orders_list)):
                if not_verified_orders_list[i][0] == order_id:
                    not_verified_orders_list.pop(i)
                    break
            bot.send_message(call.message.chat.id, "Заказ ID=" + str(order_id) + " удалён. Выберите следующий", reply_markup=not_verified_slider_keyboard(not_verified_orders_list, 0))

    if call.data[:2] == "fb":
        feedback_number = call.data.split("*")
        feedback_number = int(feedback_number[1])
        text = get_text_from_feedback_dict(feedback_number)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=feedbacks_slider_keyboard(feedback_number))

    if call.data[:5] == "ml_sh":
        order_id = call.data.split(":")
        order_id = int(order_id[1])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите клиннера которого хотите назначить", reply_markup=choose_cleaner_keyboard(order_id))

    if call.data[:2] == "cl":
        temp = call.data.split(":")
        temp = temp[1].split("*")
        cleaner_id = int(temp[0])
        order_id = int(temp[1])
        is_empty, text = (manual_assign_cleaner_to_order(cleaner_id, order_id))
        if not is_empty:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text, reply_markup=choose_cleaner_keyboard(order_id))
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            for i in range(len(not_verified_orders_list)):
                if not_verified_orders_list[i][0] == order_id:
                    with open('orders/' + str(order_id) + ".json", 'w', encoding='utf-8') as f:
                        not_verified_orders_list[i][1]["cleaner"] = cleaner_id
                        json.dump(not_verified_orders_list[i][1], f, ensure_ascii=False, indent=4)
                        f.close()
                        customer_id = not_verified_orders_list[i][1]["user_id"]
                        if not is_admin(customer_id):
                            text_for_user = "Здравствуйте " + str(not_verified_orders_list[i][1]["contact_info"]["name"]) + "!\nВаш заказ " + str(order_id) + " обработан\n" +\
                                "Ваш клиннер " + str(cleaner_id) + "\nКонтакт менеджера @Serj_you\nТелефон +375 25 111 11 11"
                            bot.send_message(not_verified_orders_list[i][1]["user_id"], text_for_user)
                        not_verified_orders_list.pop(i)
                        break
            bot.send_message(call.message.chat.id, text, reply_markup=successful_cleaner_assign_keyboard)

    if call.data[:8] == "schedule":
        number_page = call.data.split("*")
        number_page = int(number_page[1])
        bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id, reply_markup=schedule_slider_keyboard(call.message.chat.id,number_page))

    if call.data[:9] == "sc_return":
        number_page = call.data.split("*")
        number_page = int(number_page[1])
        bot.delete_message(call.message.chat.id,call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите день недели\n🔴 - есть заказы\n⚪ - нет заказов",
                         reply_markup=schedule_slider_keyboard(call.message.chat.id, number_page))

    if call.data[:4] == "scwd":
        work_day = call.data.split("*")
        work_day = work_day[1].split(":")
        number_page = work_day[1]
        work_day = work_day[0]
        bot.delete_message(call.message.chat.id,call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите заказ для просмотра подробностей", reply_markup=schedule_view_work_day(call.message.chat.id, work_day, number_page))

    if call.data[:8] == "sc_order":
        temp = call.data.split("*")
        temp = temp[1].split(":")
        order_id = temp[0]
        work_day = temp[1]
        number_page = temp[2]
        order_dict = get_order_dict_from_json_by_id(order_id)
        if len(order_dict.keys()) > 0:
            text = get_text_from_order_dict(order_dict)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_photo(call.message.chat.id, "https://i.ytimg.com/vi/OVT90uo-fmQ/maxresdefault.jpg", text, reply_markup=cleaner_view_order_keyboard(order_id, work_day, number_page, order_dict))
        else:
            bot.send_message(call.message.chat.id, "Данный заказ не найден", reply_markup=thanks_keyboard)

    if call.data[:4] == "done":
        order_id = call.data.split("*")
        order_id = int(order_id[1])
        order_dict = get_order_dict_from_json_by_id(order_id)
        order_dict["is_done"] = True
        update_order_json_from_dict(order_id, order_dict)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,"Благодарим за работу.")
        bot.send_message(order_dict["user_id"], "Ваш заказ на уборку - №" + str(order_id) + " выполнен.\nЖелаете оставить отзыв?", reply_markup=ask_to_feedback_keyboard(order_id))


    if call.data[:10] == "cutomer_fb":
        order_id = call.data.split("*")
        order_id = order_id[1]
        bot.delete_message(call.message.chat.id,call.message.message_id)
        m = bot.send_message(call.message.chat.id, "Отправьте текстовым сообщением ниже - ваш отзыв")
        bot.register_next_step_handler(m, cath_feed_back, order_id)

    if call.data[:9] == "accept_fb":
        order_id = call.data.split("*")
        order_id = int(order_id[1])
        save_feedback(order_id, call.message.text)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Отзыв сохранён",reply_markup=exit_keyboard)


    if call.data[:7] == "day_off":
        bot.answer_callback_query(call.id, "В этот день выходной", show_alert=False)


print("Ready")
bot.infinity_polling()