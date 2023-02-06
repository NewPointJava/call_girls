import time

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from keyboards import price_1st_step
from service_function import cost_calculation_st1, order_card
from settings import bot, room_price, bathroom_price, check_in_price


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ниже будет представлен расчёт стоимости.\nВы можете увеличивать и уменьшать количество комнат и санузлов.\n Стоимость будет меняться автоматически")
    bot.send_message(message.chat.id, f'1 - комната 1 - санузел = {room_price + bathroom_price + check_in_price}', reply_markup=price_1st_step(1, 1))


@bot.callback_query_handler(func=lambda call: True)
def call(call):
    #print(call)
    print(call.data)
    if call.data[:2] == "qt":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data[:3] == "st1":
        print("Логика расчёта стоимости")
        if call.data[3] != "$":
            new_text, room_amount, bathroom_amount = cost_calculation_st1(call.data)
            bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id, reply_markup=price_1st_step(room_amount, bathroom_amount))

        if call.data[3] =="$":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            time_order = time.asctime()
            caption = order_card(call.data, time_order,4)
            bot.send_photo(call.message.chat.id, "https://kartinkin.net/uploads/posts/2021-07/1626169458_2-kartinkin-com-p-uborka-art-art-krasivo-3.jpg", caption)


print("Ready")
bot.infinity_polling()