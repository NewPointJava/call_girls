from keyboards import thanks_keyboard, send_order_to_admin
from settings import bot, orders


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
        text[-1] = "\nЕсли всё верно - ☑️нажмите /continue "
        text.insert(len(text), "\nчтобы изменить адрес нажмите /address")
        text.insert(len(text), "чтобы изменить номер дома нажмите /house_number")
        text.insert(len(text), "чтобы изменить номер квартиры нажмите /flat_number")
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
        print(orders[message.chat.id])
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        try:
            bot.edit_message_caption(orders[message.chat.id], message.chat.id, order_id,reply_markup=send_order_to_admin)
        except:
            bot.send_photo(message.chat.id,
                           "https://kartinkin.net/uploads/posts/2021-07/1626169458_2-kartinkin-com-p-uborka-art-art-krasivo-3.jpg",
                           orders[message.chat.id],reply_markup=send_order_to_admin())

    elif message.content_type != "text" or message.text[0] == "/":
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        except:
            pass
        m = bot.send_message(message.chat.id,
                             "что-то пошло не так, попробуй снова написать и отправить email текстом\nДля выхода пришли '/stop")
        bot.register_next_step_handler(m, cath_email, text, m_id, order_id)


