
from keyboards import thanks_keyboard,send_order_to_admin_keyboard,admin_check_order_keyboard,accept_feedback_keyboard
from service_function import from_caption_to_dict, get_text_from_order_dict, is_admin
from get_and_set_json_information import get_and_set_order_id_from_json
from settings import bot, orders, admins, not_verified_orders_list


def cath_addres(message, text, m_id, order_id):
    if message.text == "/stop":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.delete_message(message.chat.id, m_id)
        except:
            pass
        bot.send_message(message.chat.id,
                         "Вы вышли из оформления заказа\n/new_order - для создания заказа\n/view_feedbacks - для просмотра отзывов\n/info - для дополнительной иформации о компании",
                         reply_markup=thanks_keyboard)

    elif message.content_type == "text" and message.text[0] != "/":
        text = text.split("\n")
        text[0] = "Улица: " + message.text
        text.pop()
        text.insert(len(text), "\nОтлично! Теперь отправьте сообщением номер дома ⬇️")
        text = "\n".join(text)
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, text)
            m_id = m.message_id
        bot.register_next_step_handler(m, cath_house_number, text, m_id, order_id)

    if message.content_type != "text" or message.text[0] == "/":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        m = bot.send_message(message.chat.id,
                             "Что-то пошло не так упс\nПопробуй снова написать и отправить улицу текстом\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_addres, text, m_id, order_id)




def cath_house_number(message, text, m_id, order_id):
    if message.text == "/stop":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, m_id)
        except:
            pass
        bot.send_message(message.chat.id,
                         "Вы вышли из оформления заказа\n" + \
                         "/new_order - для создания заказа\n" + \
                         "/view_feedbacks - для просмотра отзывов\n" + \
                         "/info - для дополнительной иформации о компании",
                         reply_markup=thanks_keyboard)

    elif message.content_type == "text" and message.text[0] != "/":
        text = text.split("\n")
        text[1] = "Дом: " + message.text
        text.pop()
        text[-1] = "\nОтлично! Теперь отправьте сообщением номер квартиры⬇️"
        text = "\n".join(text)
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, text)
            m_id = m.message_id
        bot.register_next_step_handler(m, cath_flat_number, text, m_id, order_id)

    if message.content_type != "text" or message.text[0] == "/":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        m = bot.send_message(message.chat.id,
                             "Что-то пошло не так упс\nПопробуй снова написать и отправить номер дома текстом\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_house_number, text, m_id, order_id)






def cath_flat_number(message, text, m_id, order_id):
    if message.text == "/stop":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.delete_message(message.chat.id, m_id)
        except:
            pass
        bot.send_message(message.chat.id,
                         "Вы вышли из оформления заказа\n/new_order - для создания заказа\n/view_feedbacks - для просмотра отзывов\n/info - для дополнительной иформации о компании",
                         reply_markup=thanks_keyboard)

    elif message.content_type == "text" and message.text[0] != "/":
        text = text.split("\n")
        text[2] = "Квартира: " + message.text

        old_text = "\n".join(text)

        text.pop()
        text[-1] = "\n\n\nЕсли всё верно - ☑️️нажмите /continue "
        text.insert(len(text)-1, "\n/address нажмите чтобы изменить адрес")
        text.insert(len(text)-1, "/house_number нажмите чтобы изменить номер дома")
        text.insert(len(text)-1, "/flat_number  нажмите чтобы изменить номер квартиры")
        text = "\n".join(text)
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, text)
            m_id = m.message_id
        bot.register_next_step_handler(m, contact_info, text, m_id, old_text, order_id)

    if message.content_type != "text" or message.text[0] == "/":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        m = bot.send_message(message.chat.id,
                             "Что-то пошло не так упс\nПопробуй снова написать и отправить номер дома текстом\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_flat_number, text, m_id, order_id)


def contact_info(message, text, m_id, old_text, order_id):
    if message.text == "/stop":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.delete_message(message.chat.id, m_id)
        except:
            pass
        bot.send_message(message.chat.id,
                         "Вы вышли из оформления заказа\n/new_order - для создания заказа\n/view_feedbacks - для просмотра отзывов\n/info - для дополнительной иформации о компании",
                         reply_markup=thanks_keyboard)
    elif message.text == "/address":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, old_text)
            m_id = m.message_id
        bot.register_next_step_handler(m, cath_addres, old_text, m_id, order_id)

    elif message.text == "/house_number":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, text)
            m_id = m.message_id
        bot.register_next_step_handler(m, cath_house_number, old_text, m_id, order_id)

    elif message.text == "/flat_number":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, text)
            m_id = m.message_id
        bot.register_next_step_handler(m, cath_flat_number, old_text, m_id, order_id)

    elif message.text == "/continue":
        text = text.split('\n')
        orders[message.chat.id] = orders[message.chat.id] + "\n\nАдрес\n" + text[0] + "\n" + text[1] + "\n" + text[2]
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.edit_message_caption(orders[message.chat.id], message.chat.id, order_id)
        except:
            bot.send_photo(message.chat.id,
                           "https://kartinkin.net/uploads/posts/2021-07/1626169458_2-kartinkin-com-p-uborka-art-art-krasivo-3.jpg",
                           orders[message.chat.id])

        text = 'Контактная информация\n\nФИО:\nКонтактный телефон:\nEmail:\n\nОтправьте сообщением ваше ФИО ⬇️'
        m = bot.send_message(message.chat.id, text)
        m_id = m.message_id
        bot.register_next_step_handler(m, cath_full_name, text, m_id, order_id)

    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass

        m = bot.send_message(message.chat.id, "Нажмите на синию надпись :)\nЕсли всё верно - ☑️нажмите /continue\n\n" +\
                             "чтобы изменить адрес нажмите /address\n" +\
                             "чтобы изменить номер дома нажмите /house_number\n" +\
                             "чтобы изменить номер квартиры нажмите /flat_number\n\n" +\
                             "чтобы выйти нажмите \stop")
        bot.register_next_step_handler(m, contact_info, text, m_id, old_text, order_id)








def cath_full_name(message, text, m_id, order_id):
    if message.text == "/stop":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.delete_message(message.chat.id, m_id)
        except:
            pass
        bot.send_message(message.chat.id,
                         "Вы вышли из оформления заказа\n/new_order - для создания заказа\n/view_feedbacks - для просмотра отзывов\n/info - для дополнительной иформации о компании",
                         reply_markup=thanks_keyboard)

    elif message.content_type == "text" and message.text[0] != "/":
        text = text.split("\n")
        text[2] = "ФИО: " + message.text
        text.pop()
        text.insert(len(text), "\nОтлично! Теперь отправьте сообщением контактный телефон (+375 25 111 11 11)⬇️")
        text = "\n".join(text)
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, text)
            m_id = m.message_id
        bot.register_next_step_handler(m, cath_phone_number, text, m_id, order_id)

    elif message.content_type != "text" or message.text[0] == "/":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        m = bot.send_message(message.chat.id,
                             "что-то пошло не так, попробуй снова написать и отправить ФИО текстом\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_full_name, text, m_id, order_id)


def cath_phone_number(message, text, m_id, order_id):
    if message.text == "/stop":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.delete_message(message.chat.id, m_id)
        except:
            pass
        bot.send_message(message.chat.id,
                         "Вы вышли из оформления заказа\n/new_order - для создания заказа\n/view_feedbacks - для просмотра отзывов\n/info - для дополнительной иформации о компании",
                         reply_markup=thanks_keyboard)

    elif message.content_type == "text" and message.text[0] != "/":
        text = text.split("\n")
        text[3] = "Телефон: " + message.text
        text.pop()
        text.insert(len(text), "\nОтлично! Теперь отправьте сообщением ваш email example@google.com⬇️")
        text = "\n".join(text)
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            m = bot.edit_message_text(text, message.chat.id, m_id)
        except:
            m = bot.send_message(message.chat.id, text)
            m_id = m.message_id
        bot.register_next_step_handler(m, cath_email, text, m_id, order_id)

    elif message.content_type != "text" or message.text[0] == "/":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        m = bot.send_message(message.chat.id,
                             "что-то пошло не так, попробуй снова написать телефонный номер текстом\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_phone_number, text, m_id, order_id)

def cath_email(message, text, m_id, order_id):
    if message.text == "/stop":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.delete_message(message.chat.id, m_id)
        except:
            pass
        bot.send_message(message.chat.id,
                         "Вы вышли из оформления заказа\n/new_order - для создания заказа\n/view_feedbacks - для просмотра отзывов\n/info - для дополнительной иформации о компании",
                         reply_markup=thanks_keyboard)

    elif message.content_type == "text" and message.text[0] != "/":
        text = text.split('\n')
        text.pop()
        text.pop(1)
        text[3] = "Email: " + message.text
        text = "\n".join(text)
        orders[message.chat.id] = orders[message.chat.id] + "\n\n" + text
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass

        if not is_admin(message.chat.id):
            try:
                bot.edit_message_caption(orders[message.chat.id], message.chat.id, order_id, reply_markup=send_order_to_admin_keyboard)
            except:
                bot.send_photo(message.chat.id,
                               "https://kartinkin.net/uploads/posts/2021-07/1626169458_2-kartinkin-com-p-uborka-art-art-krasivo-3.jpg",
                               orders[message.chat.id], reply_markup=send_order_to_admin_keyboard())
        else:
            bot.delete_message(message.chat.id, order_id)
            order_id = get_and_set_order_id_from_json()
            order_dict = from_caption_to_dict(orders[message.chat.id])
            order_dict["user_id"] = message.chat.id
            order_dict["user_name"] = message.from_user.username
            order_dict["is_created_by_admin"] = True
            not_verified_orders_list.append([order_id, order_dict])
            text_order = get_text_from_order_dict(order_dict)
            bot.send_photo(message.chat.id, "https://i.artfile.ru/1920x1200_645851_[www.ArtFile.ru].jpg", text_order, reply_markup=admin_check_order_keyboard(order_id))


    elif message.content_type != "text" or message.text[0] == "/":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        m = bot.send_message(message.chat.id,
                             "что-то пошло не так, попробуй снова написать и отправить email текстом\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_email, text, m_id, order_id)


def cath_feed_back(message, order_id):
    if message.text == "/stop":
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id,
                         "Вы вышли из заполнения отзыва",
                         reply_markup=thanks_keyboard)

    elif message.content_type == "text":
        feedback = message.text
        bot.send_message(message.chat.id,"Спасибо за ваш отзыв!\nВоспользуйтесь услугами КлинниБогини в следующий раз со скидкой 5%", reply_markup=thanks_keyboard)

        for x in admins:
            bot.send_message(x, "@" + message.from_user.username +" оставил отзыв на заказ №" + str(order_id) + "⬇️\n\n\"" + feedback + "\"", reply_markup=accept_feedback_keyboard(order_id))
    else:
        m = bot.send_message(message.chat.id,
                             "что-то пошло не так, попробуй снова написать и отправить отзыв. Принимается только текст\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_feed_back, order_id)