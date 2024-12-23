import telebot
import database as db
from buttons import *
from bts_offices import offices, kitob_post

from keep_alive import keep_alive
keep_alive()

from reques_to_site import schedule_updater
from threading import Thread
updater_thread = Thread(target=schedule_updater)
updater_thread.daemon = True
updater_thread.start()


BOT_TOKEN = '7158493029:AAHs8WxBKJxw9yV4V85L80QoyW4LGBwhYr0'
book_group_id = -4614622677
course_group_id = -4705809842

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


user_data = {}
user_selected_courses = {}
carts = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Assalomu alaykum.\nMen kitob va kurslarni sotish botiman!\n")
    bot.send_message(user_id, "Iltimos, ismingizni yuboring\n")

    bot.register_next_step_handler(message, get_name)

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
        bot.send_message(user_id, "pastdagi tugmalar orqali harakatni tanlang", reply_markup=main_menu())
        db.add_user(name, phone_number, user_id)
    else:
        bot.send_message(user_id, "Raqamingizni pastdagi tugma orqali yuboring",
                         reply_markup=phone_button_uz())
        bot.register_next_step_handler(message, contact_handler, name)
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

        payment_details = (
            "To‘lov uchun rekvizitlar:\n"
            "Karta raqam: 8600332962634972\n" 
            "Dilafruz Xidoyatova\n"
            f"To‘lovni amalga oshirilgach, <b>tasdiqlash uchun skrinshot yuboring.</b>\n"
        )
        bot.send_message(message.chat.id, payment_details, reply_markup=payment())

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
    back_button = InlineKeyboardButton("◀️ Назад", callback_data="buy_book")
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

    payment_details = (
            "To‘lov uchun rekvizitlar:\n"
            "Karta raqam: 8600332962634972\n" 
            "Dilafruz Xidoyatova\n"
            f"To‘lovni amalga oshirilgach, <b>tasdiqlash uchun skrinshot yuboring.</b>\n"
        )
    bot.send_message(call.message.chat.id, payment_details, reply_markup=payment())
    bot.answer_callback_query(call.id)

# Обработчик нажатия на инлайн-кнопку
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
        courses_list = user_order['course'].split('</b> kursi')
        formatted_courses = '\n'.join(course + '</b> kursi' for course in courses_list if course.strip())

        admin_message = (
            "#kurs\n"
            "Yangi ariza (Kurs):\n"
            f"Foydalanuvchi: <b>{name}</b>\n"
            f"Telefon: {phone_number}\n"
            f"Username: @{message.from_user.username}\n"
            f"Kurslar:\n{user_order["course"]}\n"
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
    bot.send_message(user_id, "Mavjud kurslar:", reply_markup=kurs_btns())

@bot.callback_query_handler(func=lambda call: call.data in [
    "metod_1_5", "metod_6_10", "metod_11_15", "metod_15_20", "metod_21_25", "metod_26_30", "metod_31_35", "metod_36_40", "metod_41_45", "metod_46_50",
    "metod_1_10", "metod_11_20", "metod_21_30", "metod_31_40", "metod_41_50",
    "metod_1_20", "metod_21_40",
    "metod_1_50"])
def callback_course_handler(call):

    if call.data == "metod_1_5":
        add_to_cart(call.message.chat.id, f"1-5 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "1-5 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_6_10":
        add_to_cart(call.message.chat.id, f"6-10 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "6-10 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_11_15":
        add_to_cart(call.message.chat.id, f"11-15 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "11-15 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_15_20":
        add_to_cart(call.message.chat.id, f"15-20 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "15-20 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_21_25":
        add_to_cart(call.message.chat.id, f"21-25 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "21-25 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_26_30":
        add_to_cart(call.message.chat.id, f"26-30 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "26-30 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_31_35":
        add_to_cart(call.message.chat.id, f"31-35 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "31-35 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_36_40":
        add_to_cart(call.message.chat.id, f"36-40 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "36-40 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_41_45":
        add_to_cart(call.message.chat.id, f"41-45 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "41-45 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_46_50":
        add_to_cart(call.message.chat.id, f"46-50 interaktiv metod", int5_price)
        bot.answer_callback_query(call.id, "45-50 interaktiv metodlar savatchaga qo`shildi")

    elif call.data == "metod_1_10":
        add_to_cart(call.message.chat.id, f"1-10 interaktiv metod", int10_price)
        bot.answer_callback_query(call.id, "1-10 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_11_20":
        add_to_cart(call.message.chat.id, f"11-20 interaktiv metod", int10_price)
        bot.answer_callback_query(call.id, "1-20 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_21_30":
        add_to_cart(call.message.chat.id, f"21-30 interaktiv metod", int10_price)
        bot.answer_callback_query(call.id, "21-30 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_31_40":
        add_to_cart(call.message.chat.id, f"31-40 interaktiv metod", int10_price)
        bot.answer_callback_query(call.id, "31-40 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_41_50":
        add_to_cart(call.message.chat.id, f"41-50 interaktiv metod", int10_price)
        bot.answer_callback_query(call.id, "41-50 interaktiv metodlar savatchaga qo`shildi")

    elif call.data == "metod_1_20":
        add_to_cart(call.message.chat.id, f"1-20 interaktiv metod", int20_price)
        bot.answer_callback_query(call.id, "1-20 interaktiv metodlar savatchaga qo`shildi")
    elif call.data == "metod_21_40":
        add_to_cart(call.message.chat.id, f"21-40 interaktiv metod", int20_price)
        bot.answer_callback_query(call.id, "21-40 interaktiv metodlar savatchaga qo`shildi")

    elif call.data == "metod_1_50":
        add_to_cart(call.message.chat.id, f"1-50 interaktiv metod", int50_price)
        bot.answer_callback_query(call.id, "1-50 interaktiv metodlar savatchaga qo`shildi")



@bot.callback_query_handler(func=lambda call: call.data in [
    "menu_interaktiv", "menu_pedagogik", "kurs_ekspert",
    "kurs_shogirt", "back_kurs", "back_to_main",
    "milliy", "maqola", "tajriba", "interaktiv_5", "interaktiv_10", "interaktiv_20", "interaktiv_50", "back_to_int"])
def callback_handler(call):
    if call.data == "menu_interaktiv":
        bot.edit_message_text(
            "Interaktiv metodolarni tanlang:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=interaktiv_btns())

    elif call.data == "menu_pedagogik":
        bot.edit_message_text("Pedagogik kurslardan birini tanlang:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=pedagogik_btns())

    elif call.data == "kurs_ekspert":
        bot.send_message(
            call.message.chat.id,
            "Sizning ma'lumotlaringiz adminga yuborildi!", reply_markup=main_menu()
        )
        send_to_admin(call.message, "Ekspertlar uchun metodologiya kursi")

    elif call.data == "kurs_shogirt":
        bot.send_message(
            call.message.chat.id,
            "Sizning ma'lumotlaringiz adminga yuborildi!", reply_markup=main_menu()
        )
        send_to_admin(call.message, "Shogirtlar uchun metodologiya kursi")

    elif call.data == "back_kurs":
        bot.edit_message_text("Mavjud kurslar:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kurs_btns())

    elif call.data == "back_to_int":
        bot.edit_message_text("Mavjud kurslar:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=interaktiv_btns())

    elif call.data == "back_to_main":
        bot.send_message(call.message.chat.id, "Asosiy menyu:", reply_markup=main_menu())


    elif call.data == "milliy":
        add_to_cart(call.message.chat.id, f"<b>Milliy tarbiyaning oiladagi va ta`limdagi roli</b> kursi", milliy_price)
        bot.answer_callback_query(call.id, "'Milliy tarbiyaning oiladagi va ta`limdagi roli' kursi savatchaga qo`shildi")

    elif call.data == "maqola":
        add_to_cart(call.message.chat.id, f"<b>O`z maqolangizni chop eting</b> kursi", maqola_price)
        bot.answer_callback_query(call.id, "O`z maqolangizni chop eting' kursi savatchaga qo`shildi")

    elif call.data == "tajriba":
        add_to_cart(call.message.chat.id, f"<b>Tajribani ommalashtirish</b> kursi", tajriba_price)
        bot.answer_callback_query(call.id, "'Tajribani ommalashtirish' kursi savatchaga qo`shildi")


    elif call.data == "interaktiv_5":
        bot.edit_message_text("Interaktiv metodolar:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=interaktiv_5btn())

    elif call.data == "interaktiv_10":
        bot.edit_message_text("Interaktiv metodolar:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=interaktiv_10btn())

    elif call.data == "interaktiv_20":
        bot.edit_message_text("Interaktiv metodolar:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=interaktiv_20btn())

    elif call.data == "interaktiv_50":
        bot.edit_message_text("Interaktiv metodolar:",
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
        bot.reply_to(message, "Savatingiz bo'sh.")
        return

    cart_text = "Siz tanlagan kurslar:\n"
    total = 0
    all_courses = ''
    for item in carts[user_id]:
        all_courses += item['name']
        cart_text += f"{item['name']} - {item['price']} so'm\n"
        total += item['price'] * item['quantity']
    cart_text += f"\nJami: {total} so'm"

    bot.send_message(user_id, cart_text, reply_markup=buy())
    user_data[message.chat.id] = {"course": all_courses, "total": total}

@bot.callback_query_handler(func=lambda call: call.data == 'buy_cart')
def process_puy(call):
    user_id = call.message.chat.id
    total = 0
    for item in carts[user_id]:
        total += item['price'] * item['quantity']

    payment_details = (
        f"\nJami: {total} so‘m\n\n"
        "To‘lov uchun rekvizitlar:\n"
        "Karta raqam: 8600332962634972\n"
        "Dilafruz Xidoyatova\n"
        f"To‘lovni amalga oshirilgach, <b>tasdiqlash uchun skrinshot yuboring.</b>\n")
    bot.send_message(call.message.chat.id, payment_details, reply_markup=payment())
    carts[user_id] = []

@bot.callback_query_handler(func=lambda call: call.data =='clear_cart')
def clear_cart(call):
    user_id = call.message.chat.id
    carts[user_id] = []
    bot.reply_to(call.message, "Корзина очищена.")


bot.polling()
