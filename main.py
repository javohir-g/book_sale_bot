import threading
import time

import telebot
from telebot.types import InputMediaPhoto

import database as db
from buttons import *
from bts_offices import offices
from price import *
from keep_alive import keep_alive
keep_alive()

from reques_to_site import schedule_updater
from threading import Thread
updater_thread = Thread(target=schedule_updater)
updater_thread.daemon = True
updater_thread.start()


BOT_TOKEN = '7849986414:AAG0uwBw_WsPbouwjI1hu9twfgzNZbObhw0'
book_group_id = -1002446300095
course_group_id = -1002481066762

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


user_data = {}

user_selected_courses = {}
carts = {}

DELETE_VIDEO_TIME = 300  # 5 минут
REMINDER_INTERVAL = 30  # 1 минута

YOUTUBE_VIDEO_LINK = "https://youtu.be/YOUR_VIDEO_ID"  # Ваша ссылка на видео
FILE_PATH = "kurs_prezentatsiya.pdf"  # Путь к файлу для отправки




CHANNEL_USERNAME = "@dilafruz_xidoyatova"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    with open("photos/original-10e802655408a32655ad03089a7208b0.mp4", "rb") as video:
        bot.send_video(user_id, video=video, caption="Assalomu alaykum.\nMen Dilafruz Xidoyatovaning kitob va kurslarni sotuvchi botiman!")
    bot.send_message(user_id, "Davom etish uchun kanalimizga obuna bo‘ling", reply_markup=chanal_link())

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, f"{name} tanishganimdan xursandman endi raqamingizni pastdagi tugma orqali yuboring",reply_markup=phone_button_uz())
    bot.register_next_step_handler(message, contact_handler, name)

def contact_handler(message, name):
    user_id = message.chat.id

    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "Tizimda muvaffaqiyatli ro'yxatdan o'tdingiz!")
        db.add_user(name, phone_number, user_id)
        with open("photos/original-10e802655408a32655ad03089a7208b0.mp4", "rb") as video:
            bot.send_video(user_id, video=video, caption="Botdan foydalanish bo‘yicha video qo‘llanma", reply_markup=main_menu_and_course())
    else:
        bot.send_message(user_id, "Raqamingizni pastdagi tugma orqali yuboring",
                         reply_markup=phone_button_uz())
        bot.register_next_step_handler(message, contact_handler, name)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    try:
        # Проверяем статус пользователя в канале
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ["member", "administrator", "creator"]:
            bot.answer_callback_query(call.id, "Siz kanalga obuna bo‘ldingiz! ✅")
            bot.send_message(call.message.chat.id, "Obunangiz uchun rahmat! Endi botdan foydalanishingiz mumkin. 😊")
            bot.send_message(user_id, "Iltimos, ismingizni yuboring\n")
            bot.register_next_step_handler(call.message, get_name)
        else:
            bot.answer_callback_query(call.id, "Kanalga hali obuna bo‘lmagansiz! ❌")
            bot.send_message(call.message.chat.id, "Iltimos, kanalga obuna bo‘ling va tugmani yana bir marta bosing")
    except Exception as e:
        bot.answer_callback_query(call.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")
        bot.send_message(call.message.chat.id, f"Ошибка: {e}")


#----------kitob----------------
@bot.message_handler(func=lambda message: message.text == "📚 Kitob")
def book_type(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Qaysi kitobni sotib olmoqchisiz", reply_markup=kitob_menu())

@bot.message_handler(func=lambda message: message.text in ["📘 Samarali interaktiv metodlar 1.0", "📕 Samarali interaktiv metodlar 2.0", "⬅️ Orqaga"])
def books(message):
    user_id = message.from_user.id
    if message.text == "📘 Samarali interaktiv metodlar 1.0":
        with open('photos/photo_2023-10-12_15-56-29.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=kitob_post, reply_markup=kitob_buy())

    elif message.text == "📕 Samarali interaktiv metodlar 2.0":
        bot.send_message(user_id, "tez orada", reply_markup=main_menu())

    elif message.text == "⬅️ Orqaga":
        bot.send_message(user_id, "Аsosiy menyu", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data == "buy_book")
def delivery_selection(call):
    try:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kitob_delivery()
        )
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(
            call.message.chat.id,
            "Yetkazib berish usulini tanlang:",
            reply_markup=kitob_delivery()
        )

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "yandex_delivery")
def request_location(call):
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Iltimos, joylashuvingizni yuboring"
        )
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(
            call.message.chat.id,
            "Iltimos, joylashuvingizni yuboring",
            reply_markup=location_btn()
        )

    user_data[call.message.chat.id] = {"delivery_type": "yandex"}
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.chat.id in user_data and user_data[message.chat.id].get("delivery_type") == "yandex":
        user_data[message.chat.id]["location"] = message.location

        payment_details = "To‘lov usulini tanlang."
        bot.send_message(message.chat.id, payment_details, reply_markup=payment())

        time.sleep(5)
        bot.send_message(message.chat.id, f"To‘lovni amalga oshirilgach, <b>tasdiqlash uchun skrinshot yuboring.</b>\n")

@bot.callback_query_handler(func=lambda call: call.data == "bts_delivery")
def select_bts_region(call):
    markup = InlineKeyboardMarkup(row_width=2)
    for region in offices.keys():
        button = InlineKeyboardButton(region, callback_data=f"region_{region}")
        markup.add(button)

    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Hududni tanlang:"
        )
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(
            call.message.chat.id,
            "Hududni tanlang:",
            reply_markup=markup
        )

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("region_"))
def select_bts_office(call):
    region = call.data.split("_")[1]
    markup = InlineKeyboardMarkup(row_width=2)

    for office in offices[region]:
        button = InlineKeyboardButton(office, callback_data=f"office_{office}")
        markup.add(button)

    # Добавляем кнопку "Назад"
    back_button = InlineKeyboardButton("◀️ Orqaga", callback_data="buy_book")
    markup.add(back_button)

    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Hududdagi ofisni tanlang {region}:"
        )
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(
            call.message.chat.id,
            f"Hududdagi ofisni tanlang {region}:",
            reply_markup=markup
        )

    user_data[call.message.chat.id] = {"delivery_type": "bts", "region": region}
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("office_"))
def bts_payment(call):
    office = call.data.split("_", 1)[1]
    user_data[call.message.chat.id]["office"] = office

    payment_details = "To‘lov usulini tanlang."
    bot.send_message(call.message.chat.id, payment_details, reply_markup=payment())
    bot.answer_callback_query(call.id)

    time.sleep(5)
    bot.send_message(call.message.chat.id, f"To‘lovni amalga oshirilgach, <b>tasdiqlash uchun skrinshot yuboring.</b>\n")

@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def handle_order_status_change(call):
    callback_data = call.data
    user_id, status = callback_data.split("_")[1], callback_data.split("_")[2]

    if status == "pending":
        # Меняем статус на обработано
        new_markup = InlineKeyboardMarkup()
        new_button = InlineKeyboardButton("✅ariza qabul qilindi✅", callback_data=f"order_{user_id}_processed")
        new_markup.add(new_button)

        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=new_markup
        )

    elif status == "processed":
        bot.answer_callback_query(call.id, "Заявка уже обработана.")

@bot.message_handler(content_types=['photo'])
def handle_payment_confirmation(message):
    user_id = message.chat.id
    user_info = db.get_user(user_id)

    if not user_info:
        bot.send_message(user_id, "Ma'lumotlaringiz tizimda topilmadi. /start buyrug'i orqali qayta ro'yxatdan o'ting.")
        return

    name = user_info["name"]
    phone_number = user_info["phone_number"]

    user_order = user_data.get(user_id, {})

    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("❌ariza qabul qilinmagan❌", callback_data=f"order_{user_id}_pending")
    markup.add(button)

    if "course" in user_order:
        courses_list = user_order['course'].replace(".", "\n")
        admin_message = (
            "#kurs\n"
            "Yangi ariza (Kurs):\n"
            f"Foydalanuvchi: <b>{name}</b>\n"
            f"Telefon: {phone_number}\n"
            f"Username: @{message.from_user.username}\n"
            f"Kurslar:\n{courses_list}\n"
            f"Jami summa: {user_order['total']} so'm"
        )
        bot.send_photo(
            course_group_id,
            message.photo[-1].file_id,
            caption=admin_message,
            reply_markup=markup
        )
        bot.send_message(user_id, "Arizangiz administratorga yuborildi. Tez orada siz bilan bog'lanamiz.",
                         reply_markup=main_menu())

    elif "delivery_type" in user_order:
        if user_order.get("delivery_type") == "yandex":
            admin_message = (
                "#yandex #kitob\n"
                "Yangi ariza (Yandex Yetkazib berish):\n"
                f"Foydalanuvchi: <b>{name}</b>\n"
                f"Telefon: {phone_number}\n"
                f"Username: @{message.from_user.username}\n"
                f"Manzil: ⬇️"
            )
            bot.send_photo(book_group_id, message.photo[-1].file_id, caption=admin_message, reply_markup=markup)
            bot.send_location(book_group_id, user_order['location'].latitude, user_order['location'].longitude)

        elif user_order.get("delivery_type") == "bts":
            admin_message = (
                "#bts #kitob\n"
                "Yangi ariza (BTS Yetkazib berish):\n"
                f"Foydalanuvchi: <b>{name}</b>\n"
                f"Telefon: {phone_number}\n"
                f"Username: @{message.from_user.username}\n"
                f"Hudud: {user_order.get('region', 'Kiritilmagan')}\n"
                f"Ofis: {user_order.get('office', 'Kiritilmagan')}"
            )
            bot.send_photo(
                book_group_id,
                message.photo[-1].file_id,
                caption=admin_message,
                reply_markup=markup
            )
        bot.send_message(user_id, "Arizangiz administratorga yuborildi. Tez orada siz bilan bog'lanamiz.",
                         reply_markup=main_menu())

    else:
        bot.send_message(user_id, "Buyurtma topilmadi. Iltimos, qaytadan urinib ko'ring.")

#-------free_course------------

@bot.message_handler(func=lambda message: message.text == "✅ Bepul video dars")
def send_video(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Сохраняем данные пользователя
    user_data[user_id] = {
        "watched": False,
        "start_time": time.time(),
        "last_reminder": time.time(),
        "message_ids": [],
        "reminder_messages": [],  # Храним ID напоминательных сообщений
    }

    # Отправляем ссылку на видео
    msg = bot.send_message(chat_id, f"Bepul video darsga havola: {YOUTUBE_VIDEO_LINK}")
    user_data[user_id]["message_ids"].append(msg.message_id)

    # Запускаем таймер для напоминаний через 1 минуту
    threading.Thread(target=send_reminders, args=(chat_id, user_id), daemon=True).start()


def send_reminders(chat_id, user_id):
    # Напоминания каждую минуту с указанием оставшегося времени
    # Создаём инлайн-кнопки
    inline_markup = InlineKeyboardMarkup()
    inline_markup.add(
        InlineKeyboardButton("Ko‘rdim", callback_data="watched"),
        InlineKeyboardButton("Ko‘rmadim", callback_data=f"not_watched")
    )

    for remaining_minutes in range(4, 0, -1):  # 4, 3, 2, 1
        time.sleep(30)  # Ждём 1 минуту
        if user_data.get(user_id) and not user_data[user_id]["watched"]:
            reminder_msg = bot.send_message(chat_id,
                                            f"Havolalar yopilishiga {remaining_minutes} daqiqa qoldi.", reply_markup=inline_markup)
            user_data[user_id]["reminder_messages"].append(reminder_msg.message_id)

    # После 5 минут удаляем все сообщения и кнопку
    time.sleep(30)  # Ждём еще 1 минуту
    if user_data.get(user_id) and not user_data[user_id]["watched"]:

        for msg_id in user_data[user_id]["message_ids"]:
            try:
                bot.delete_message(chat_id, msg_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {msg_id}: {e}")

        # Удаляем все напоминания
        for reminder_msg_id in user_data[user_id]["reminder_messages"]:
            try:
                bot.delete_message(chat_id, reminder_msg_id)
            except Exception as e:
                print(f"Ошибка при удалении напоминания {reminder_msg_id}: {e}")

        user_data.pop(user_id, None)

@bot.callback_query_handler(func=lambda call: call.data in ["watched", "not_watched"])
def handle_video_response(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if call.data == "watched":
        # Пользователь посмотрел видео
        user_data[user_id]["watched"] = True
        bot.send_message(chat_id, "Videoni ko‘rganingiz uchun rahmat",reply_markup=main_menu())
        with open(FILE_PATH, "rb") as file:
            bot.send_document(chat_id, file)

    elif call.data == "not_watched":
        # Пользователь не посмотрел видео
        bot.send_message(chat_id, f"{YOUTUBE_VIDEO_LINK}\n👆 Videoni tomosha qilgandan keyin 'Ko‘rdim' tugmasini bosing")
        threading.Thread(target=send_reminders, args=(chat_id, user_id), daemon=True).start()




#--------admin_message----------
def send_to_admin(message, course_name):
    user_id = message.chat.id
    user_info = db.get_user(user_id)  # Получаем данные пользователя из базы
    name = user_info["name"]
    phone_number = user_info["phone_number"]

    user_info = (f"Foydalanuvchi: {name}\n"
                 f"Username: @{message.chat.username}\n"
                 f"Telefon raqam: {phone_number}\n"
                 f"Kurs: {course_name}")
    bot.send_message(course_group_id, user_info)

#---------------kurs-------------------
@bot.message_handler(func=lambda message: message.text == "💻 Kurslar")
def kurs_menu(message):
    user_id = message.from_user.id
    with open('photos/21.png', 'rb') as photo:
        bot.send_photo(user_id, photo, reply_markup=kurs_btns())

@bot.callback_query_handler(func=lambda call: call.data in [
    "toplam1", "toplam2", "toplam3", "toplam4", "toplam5", "toplam6", "toplam7", "toplam8", "toplam9", "toplam10",
    "toplam1_to_cart_btn", "toplam2_to_cart_btn", "toplam3_to_cart_btn", "toplam4_to_cart_btn", "toplam5_to_cart_btn", "toplam6_to_cart_btn", "toplam7_to_cart_btn", "toplam8_to_cart_btn", "toplam9_to_cart_btn", "toplam10_to_cart_btn" ])
def callback_course5_handler(call):
    from telebot.types import InputMediaPhoto
    if call.data == "toplam1":
        photo = open("photos/24.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn1()
        )
    elif call.data == "toplam1_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>1chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "1chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam2":
        photo = open("photos/25.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn2()
        )
    elif call.data == "toplam2_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>2chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "2chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam3":
        photo = open("photos/26.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn3()
        )
    elif call.data == "toplam3_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>3chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "3chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam4":
        photo = open("photos/27.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn4()
        )
    elif call.data == "toplam4_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>4chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "4chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam5":
        photo = open("photos/28.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn5()
        )
    elif call.data == "toplam5_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>5chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "5chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam6":
        photo = open("photos/29.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn6()
        )
    elif call.data == "toplam6_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>6chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "6chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam7":
        photo = open("photos/30.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn7()
        )
    elif call.data == "toplam7_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>7chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "7chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam8":
        photo = open("photos/31.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn8()
        )
    elif call.data == "toplam8_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>8chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "8chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam9":
        photo = open("photos/32.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn9()
        )
    elif call.data == "toplam9_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>9chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "9chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())

    elif call.data == "toplam10":
        photo = open("photos/33.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_5ta_btn10()
        )
    elif call.data == "toplam10_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>10chi 5ta metodlar to‘plami.</b>", int5_price)
        bot.answer_callback_query(call.id, "10chi 5ta metodlar to‘plami savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data in [
    "toplam1_2", "toplam3_4", "toplam5_6", "toplam7_8", "toplam9_10",
    "toplam10_1_to_cart_btn", "toplam10_2_to_cart_btn", "toplam10_3_to_cart_btn", "toplam10_4_to_cart_btn", "toplam10_5_to_cart_btn"])
def callback_course10_handler(call):
    if call.data == "toplam1_2":
        photo = open("photos/35.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_10ta_btn1())

    elif call.data == "toplam10_1_to_cart_btn":
        bot.answer_callback_query(call.id, "1chi 10ta metodli to‘plam savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>1chi 10ta metodli to‘plam.</b>", int10_price)
        bot.send_message(call.message.chat.id, "<b>1chi 10ta metodli to‘plam</b> savatchaga qo`shildi", reply_markup=main_menu())

    elif call.data == "toplam3_4":
        photo = open("photos/36.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_10ta_btn2())

    elif call.data == "toplam10_2_to_cart_btn":
        bot.answer_callback_query(call.id, "2chi 10ta metodli to‘plam savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>2chi 10ta metodli to‘plam.</b>", int10_price)
        bot.send_message(call.message.chat.id, "<b>2chi 10ta metodli to‘plam</b> savatchaga qo`shildi", reply_markup=main_menu())

    elif call.data == "toplam5_6":
        photo = open("photos/37.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_10ta_btn3())

    elif call.data == "toplam10_3_to_cart_btn":
        bot.answer_callback_query(call.id, "3chi 10ta metodli to‘plam savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>3chi 10ta metodli to‘plam.</b>", int10_price)
        bot.send_message(call.message.chat.id, "<b>3chi 10ta metodli to‘plam</b> savatchaga qo`shildi", reply_markup=main_menu())

    elif call.data == "toplam7_8":
        photo = open("photos/38.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_10ta_btn4())

    elif call.data == "toplam10_4_to_cart_btn":
        bot.answer_callback_query(call.id, "4chi 10ta metodli to‘plam savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>4chi 10ta metodli to‘plam.</b>", int10_price)
        bot.send_message(call.message.chat.id, "<b>4chi 10ta metodli to‘plam</b> savatchaga qo`shildi", reply_markup=main_menu())

    elif call.data == "toplam9_10":
        photo = open("photos/39.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_10ta_btn5())

    elif call.data == "toplam10_5_to_cart_btn":
        bot.answer_callback_query(call.id, "5chi 10ta metodli to‘plam savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>5chi 10ta metodli to‘plam.</b>", int10_price)
        bot.send_message(call.message.chat.id, "<b>5chi 10ta metodli to‘plam</b> savatchaga qo`shildi", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data in [
    "toplam1_25", "toplam26_50",
    "toplam25_1_to_cart_btn", "toplam25_2_to_cart_btn"])
def callback_course25_handler(call):
    if call.data == "toplam1_25":
        photo = open("photos/41.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_25ta_btn1())

    elif call.data == "toplam25_1_to_cart_btn":
        bot.answer_callback_query(call.id, "1chi 25ta metodli to‘plam savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>1chi 25ta metodli to‘plam.</b>", int20_price)
        bot.send_message(call.message.chat.id, "<b>1chi 25ta metodli to‘plam</b> savatchaga qo`shildi", reply_markup=main_menu())

    elif call.data == "toplam26_50":
        photo = open("photos/42.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=toplam_25ta_btn2())

    elif call.data == "toplam25_2_to_cart_btn":
        bot.answer_callback_query(call.id, "2chi 25ta metodli to‘plam savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>2chi 25ta metodli to‘plam.</b>", int20_price)
        bot.send_message(call.message.chat.id, "<b>2chi 25ta metodli to‘plam</b> savatchaga qo`shildi", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data in [
    "toplam1_50",
    "toplam50_1_to_cart_btn"])
def callback_course50_handler(call):
    if call.data == "toplam1_50":
        bot.edit_message_text(chat_id=call.message.chat.id, text=info_toplam_1_50, message_id=call.message.message_id)

    elif call.data == "toplam50_1_to_cart_btn":
        add_to_cart(call.message.chat.id, f"<b>50ta metodli to‘plam.</b>", int50_price)
        bot.answer_callback_query(call.id, "50ta metodli to‘plam savatchaga qo`shildi")
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data in [
    "menu_interaktiv", "menu_pedagogik", "kurs_ekspert",
    "kurs_shogirt", "back_kurs", "back_to_main", "back_kurs__",
    "milliy", "maqola", "tajriba", "lider", "interaktiv_5", "interaktiv_10", "interaktiv_20", "interaktiv_50", "back_to_int",
    "milliy_to_cart_btn", "tajriba_to_cart_btn", "maqola_to_cart_btn", "lider_to_cart_btn", "shogirt_ariza_btn", "expert_ariza_btn"])
def callback_handler(call):
    if call.data == "menu_interaktiv":
        photo = open("photos/22.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            reply_markup = interaktiv_btns())

    elif call.data == "menu_pedagogik":
        photo = open("photos/44.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=pedagogik_btns())

    elif call.data == "kurs_ekspert":
        bot.delete_message(call.message.chat.id, call.message.message_id)

        photo = open("photos/49.png", "rb")
        bot.send_photo(

            photo=photo,
            chat_id=call.message.chat.id)
        bot.send_message(chat_id=call.message.chat.id, text=expert_text, reply_markup=expert_ariza())

    elif call.data == "expert_ariza_btn":
        send_to_admin(call.message, "Ekspertlar uchun metodologik xizmat")
        bot.send_message(call.message.chat.id,"Sizning ma'lumotlaringiz adminga yuborildi!", reply_markup=main_menu())

    elif call.data == "kurs_shogirt":
        bot.delete_message(call.message.chat.id, call.message.message_id)

        photo = open("photos/50.png", "rb")
        bot.send_photo(
            photo=photo,
            chat_id=call.message.chat.id)
        bot.send_message(chat_id=call.message.chat.id, text=shogirt_text, reply_markup=shogirt_ariza())

    elif call.data == "shogirt_ariza_btn":
        send_to_admin(call.message, "Shogirtlar uchun metodologik kurs")
        bot.send_message(call.message.chat.id,"Sizning ma'lumotlaringiz adminga yuborildi!", reply_markup=main_menu())

    elif call.data == "back_kurs":
        photo = open("photos/21.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kurs_btns())

    elif call.data == "back_kurs__":
        photo = open("photos/21.png", "rb")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id-1,
            reply_markup=kurs_btns())

    elif call.data == "back_to_int":
        photo = open("photos/22.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=interaktiv_btns())

    elif call.data == "back_to_main":
        bot.send_message(call.message.chat.id, "Asosiy menyu", reply_markup=main_menu())


    elif call.data == "milliy":
        photo = open("photos/45.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=milliy_add_to_cart())

    elif call.data == "milliy_to_cart_btn":
        bot.answer_callback_query(call.id, "'Milliy tarbiyaning oiladagi va ta`limdagi roli' kursi savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>Milliy tarbiyaning oiladagi va ta`limdagi roli</b> kursi.", milliy_price)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "<b>'Milliy tarbiyaning oiladagi va ta`limdagi roli'</b> kursi savatchaga qo`shildi", reply_markup=main_menu())


    elif call.data == "maqola":
        photo = open("photos/46.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=maqola_add_to_cart())

    elif call.data == "maqola_to_cart_btn":
        bot.answer_callback_query(call.id, "'O`z maqolangizni chop eting' kursi savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>O`z maqolangizni chop eting</b> kursi.", maqola_price)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "<b>'O`z maqolangizni chop eting'</b> kursi savatchaga qo`shildi", reply_markup=main_menu())

    elif call.data == "tajriba":
        photo = open("photos/47.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=tajriba_add_to_cart())

    elif call.data == "tajriba_to_cart_btn":
        bot.answer_callback_query(call.id, "'Tajribani ommalashtirish' kursi savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>Tajribani ommalashtirish</b> kursi.", tajriba_price)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "<b>'Tajribani ommalashtirish'</b> kursi savatchaga qo`shildi",
                         reply_markup=main_menu())

    elif call.data == "lider":
        photo = open("photos/48.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=lider_add_to_cart())

    elif call.data == "lider_to_cart_btn":
        bot.answer_callback_query(call.id, "'Lider ustoz' kursi savatchaga qo`shildi")
        add_to_cart(call.message.chat.id, f"<b>Lider ustoz</b> kursi.", lider_price)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "<b>'Lider ustoz'</b> kursi savatchaga qo`shildi",
                         reply_markup=main_menu())




    elif call.data == "interaktiv_5":
        photo = open("photos/23.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=interaktiv_5btn())

    elif call.data == "interaktiv_10":
        photo = open("photos/34.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=interaktiv_10btn())

    elif call.data == "interaktiv_20":
        photo = open("photos/40.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=interaktiv_25btn())

    elif call.data == "interaktiv_50":
        photo = open("photos/43.png", "rb")
        bot.edit_message_media(
            media=InputMediaPhoto(photo),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=interaktiv_50btn())

# Функция для добавления товара в корзину
def add_to_cart(user_id, item_name, price, quantity=1):
    if user_id not in carts:
        carts[user_id] = []
    # Проверяем, есть ли уже товар в корзине
    for item in carts[user_id]:
        if item['name'] == item_name:
            #bot.answer_callback_query(call.id,"Bu kurs allaqachon savatda")

            return
    # Если товара еще нет, добавляем
    carts[user_id].append({'name': item_name, 'price': price, 'quantity': quantity})


@bot.message_handler(func=lambda message: message.text == '🗑 Savatcha')
def show_cart(message):
    user_id = message.chat.id
    if user_id not in carts or not carts[user_id]:
        bot.send_message(message.chat.id, "Savatingiz bo'sh.", reply_markup=main_menu())
        return

    cart_text = "Siz tanlagan kurslar:\n\n"
    total = 0
    all_courses = ''
    for item in carts[user_id]:
        all_courses += item['name']
        cart_text += f"{item['name']} - {item['price']} so'm\n"
        price1 = int(item['price'].replace(".",""))
        total += price1
    cart_text += f"\nJami: {total:,}".replace(",", ".") + " so'm"

    bot.send_message(user_id, cart_text, reply_markup=buy())
    user_data[message.chat.id] = {"course": all_courses, "total": total}

@bot.callback_query_handler(func=lambda call: call.data in ['buy_cart', 'card_number'])
def process_puy(call):
    user_id = call.message.chat.id
    if call.data == 'buy_cart':
        total = 0
        cart_text = ""
        all_courses = ''
        for item in carts[user_id]:
            all_courses += item['name']
            cart_text += f"{item['name']} - {item['price']} so'm\n"
            price1 = int(item['price'].replace(".", ""))
            total += price1

        payment_details = "To‘lov usulini tanlang."

        bot.send_message(call.message.chat.id, payment_details, reply_markup=payment())
        carts[user_id] = []
        time.sleep(5)
        bot.send_message(call.message.chat.id, f"To‘lovni amalga oshirilgach, <b>tasdiqlash uchun skrinshot yuboring.</b>\n")

    elif call.data == 'card_number':
        bot.send_message(call.message.chat.id,"Nusxa olish uchun katak raqamini ustiga bosing\nKarta raqami: <code>8600332962634972</code>\n<b>Dilafruz Xidoyatova</b>\n")


@bot.callback_query_handler(func=lambda call: call.data =='clear_cart')
def clear_cart(call):
    user_id = call.message.chat.id
    carts[user_id] = []
    bot.reply_to(call.message, "Savat tozalandi.")


bot.polling(non_stop=True)
