import time
from datetime import date, timedelta

from telebot.types import InlineKeyboardButton
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from keyboards import price_1st_step, st2_keyboard, choose_time_keyboard, choose_frequency_keyboard, \
    st2_frequency_keyboard, extra_service_st1_keyboard, st2_extra_service_keyboard, check_order_keyboard, \
    thanks_keyboard, not_verified_slider_keyboard
from next_step_handlers_func import cath_addres
from service_function import cost_calculation_st1, order_card, edit_order_caption_date, edit_order_caption_time, \
    edit_caption_extra_service, edit_caption_discount, from_caption_to_dict, get_order_id_from_json, is_admin, \
    get_text_from_dict_to_text
from settings import bot, room_price, bathroom_price, check_in_price, orders, not_verified_orders_list, admins, \
    test_text


@bot.message_handler(commands=['start'])
def start(message):
    text = 'Улица:\nДом:\nКвартира:\n\nОтправьте сообщением название улицы ⬇️'
    m = bot.send_message(message.chat.id, text)
    m_id = m.message_id
    bot.register_next_step_handler(m, cath_addres, text, m_id)


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

    bot.send_message(message.chat.id, text)

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
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['new_order'])
def new_order(message):
    bot.send_message(message.chat.id, "Ниже будет представлен расчёт стоимости.\nВы можете увеличивать и уменьшать количество комнат и санузлов.\n "\
            "Далее вы сможете изменять время, частоту и доп. услуги.\n\nСтоимость будет меняться автоматически", reply_markup=thanks_keyboard)
    bot.send_message(message.chat.id, f'1 - комната 1 - санузел = {room_price + bathroom_price + check_in_price}р', reply_markup=price_1st_step(1, 1))


@bot.message_handler(commands=['not_verified'])
def not_verified(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Вот список не проверенных заказов", reply_markup=not_verified_slider_keyboard(not_verified_orders_list, 0))
    else:
        bot.send_message(message.chat.id, "Вы не являетесь админом. Воспользуйтесь командной /help", reply_markup=thanks_keyboard)

@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(call):
    result, key, step = DetailedTelegramCalendar(min_date=(date.today() + timedelta(days=1)), max_date=date.today()+timedelta(days=60)).process(call.data)
    if not result and key:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,reply_markup=key)
    elif result:
        bot.edit_message_caption(edit_order_caption_date(call.message.caption, result), call.message.chat.id, call.message.message_id, reply_markup=choose_time_keyboard())
@bot.callback_query_handler(func=lambda call: True)
def call(call):
    #print(call)
    print("call data = ", call.data)
    if call.data[:2] == "qt":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data[:3] == "st1":
        if call.data[3] != "$":
            if call.data[3] != ":":
                new_text, room_amount, bathroom_amount = cost_calculation_st1(call.data)
                bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id, reply_markup=price_1st_step(room_amount, bathroom_amount))
            else:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                amount = call.data.split(":")
                amount = amount[1].split("*")
                amount[0] = int(amount[0])
                amount[1] = int(amount[1])
                bot.send_message(call.message.chat.id,
                                 f'{amount[0]} - комната {amount[1]} - санузел = {check_in_price + room_price*amount[0] + bathroom_price* amount[1]}р',
                                 reply_markup=price_1st_step(int(amount[0]), int(amount[1])))

        if call.data[3] =="$":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            time_order = time.asctime()
            caption, room_amount, bathroom_amount = order_card(call.data, time_order, 4)
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
                print("nothing to change")
        if call.data[4:] == "check_order":
            bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,reply_markup=check_order_keyboard(call.message.caption))

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
        order_id = get_order_id_from_json()
        order_dict = from_caption_to_dict(call.message.caption)
        order_dict["user_id"] = call.message.chat.id
        order_dict["user_name"] = call.from_user.username
        not_verified_orders_list.append([order_id, order_dict])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Заказ Сформирован\nID заказа - " + str(order_id) +"\n После проверки заказа и назначаем клинниров вам придёт уведомление", reply_markup=thanks_keyboard)
        try:
            for x in admins:
                bot.send_message(x, "Поступил новый заказ. ID - " + str(order_id))
        except:
            print(not_verified_orders_list)

    if call.data[:6] == "nt_ver":
        if call.data[6] == "*":
            call.data = call.data.split("*")
            number_page = int(call.data[1])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup= not_verified_slider_keyboard(not_verified_orders_list, number_page))

        elif call.data[6] == ":":
            call.data = call.data.split(":")
            order_id = int(call.data[1])
            for x in not_verified_orders_list:
                if x[0] == order_id:
                    text = get_text_from_dict_to_text(x[1])
                    #bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, "https://i.artfile.ru/1920x1200_645851_[www.ArtFile.ru].jpg", text)







print("Ready")
bot.infinity_polling()