import time
from datetime import date, timedelta

from telebot.types import InlineKeyboardButton
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from keyboards import price_1st_step, st2_keyboard, choose_time_keyboard, choose_frequency_keyboard
from service_function import cost_calculation_st1, order_card, edit_order_caption_date, edit_order_caption_time
from settings import bot, room_price, bathroom_price, check_in_price


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ниже будет представлен расчёт стоимости.\nВы можете увеличивать и уменьшать количество комнат и санузлов.\n Стоимость будет меняться автоматически")
    bot.send_message(message.chat.id, f'1 - комната 1 - санузел = {room_price + bathroom_price + check_in_price}р', reply_markup=price_1st_step(1, 1))


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
            bot.edit_message_caption(caption, call.message.chat.id,call.message.message_id, reply_markup=st2_keyboard(room_amount,bathroom_amount))

        if  call.data[4:] == "frequency":
            bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,reply_markup=choose_frequency_keyboard())



print("Ready")
bot.infinity_polling()