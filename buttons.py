from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    books = KeyboardButton("📚 Kitob")
    courses = KeyboardButton("💻 Kurslar")
    korzina = KeyboardButton("🗑 Savatcha")
    markup.add(books, courses)
    markup.add(korzina)
    return markup

def phone_button_uz():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = KeyboardButton("Telefon raqamini yuboring", request_contact=True)
    markup.add(button_phone)
    return markup

def location_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Joylashuvimni yuborish", request_location=True)
    markup.add(button)
    return markup

def kitob_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton("📘 Samarali interaktiv metodlar 1.0")
    button2 = KeyboardButton("📕 Samarali interaktiv metodlar 2.0")
    button3 = KeyboardButton("⬅️ Orqaga")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    return markup

def kitob_buy():
    markup = InlineKeyboardMarkup()
    buy_button = InlineKeyboardButton("Ushbu kitobni sotib olish", callback_data="buy_book")
    markup.add(buy_button)
    return markup

def kitob_delivery():
    markup = InlineKeyboardMarkup()
    yandex_button = InlineKeyboardButton("Yandex Доставка(Toshkent bo‘ylab)", callback_data="yandex_delivery")
    bts_button = InlineKeyboardButton("BTS Доставка(viloyatlar bo‘yicha)", callback_data="bts_delivery")
    markup.add(yandex_button)
    markup.add(bts_button)
    return markup

def payment():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Click", url="https://indoor.click.uz/pay?id=054236&t=0&amount=10000")
    button2 = InlineKeyboardButton("Payme", url="https://payme.uz/fallback/merchant/?id=65200f1f5a8224b99c9a37e3")
    markup.add(button1, button2)
    return markup

#---------------kurs-------------------
def kurs_btns():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Interaktiv metodolar", callback_data="menu_interaktiv")
    button2 = InlineKeyboardButton("Pedagogik kurs", callback_data="menu_pedagogik")
    button3 = InlineKeyboardButton("Ekspertlar uchun metodologiya kursi", callback_data="kurs_ekspert")
    button4 = InlineKeyboardButton("Shogirtlar uchun metodologiya kursi", callback_data="kurs_shogirt")
    button5 = InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_to_main")
    markup.add(button1, button2, button3, button4, button5)
    return markup

def interaktiv_btns():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("5ta metod", callback_data="interaktiv_5")
    button2 = InlineKeyboardButton("10ta metod", callback_data="interaktiv_10")
    button3 = InlineKeyboardButton("20ta metod", callback_data="interaktiv_20")
    button4 = InlineKeyboardButton("50ta metod", callback_data="interaktiv_50")
    button5 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_kurs")
    markup.add(button1, button2, button3, button4, button5)
    return markup

def interaktiv_5btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("1-5 metod", callback_data="metod_1_5")
    button2 = InlineKeyboardButton("6-10 metod", callback_data="metod_6_10")
    button3 = InlineKeyboardButton("11-15 metod", callback_data="metod_11_15")
    button4 = InlineKeyboardButton("15-20 metod", callback_data="metod_15_20")
    button5 = InlineKeyboardButton("21-25 metod", callback_data="metod_21_25")
    button6 = InlineKeyboardButton("26-30 metod", callback_data="metod_26_30")
    button7 = InlineKeyboardButton("31-35 metod", callback_data="metod_31_35")
    button8 = InlineKeyboardButton("36-40 metod", callback_data="metod_36_40")
    button9 = InlineKeyboardButton("41-45 metod", callback_data="metod_41_45")
    button10 = InlineKeyboardButton("46-50 metod", callback_data="metod_46_50")
    button11 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11)
    return markup

int5_price = 50000
int10_price = 90000
int20_price = 160000
int50_price = 350000

def interaktiv_10btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("1-10 metod", callback_data="metod_1_10")
    button3 = InlineKeyboardButton("11-20 metod", callback_data="metod_11_20")
    button5 = InlineKeyboardButton("21-30 metod", callback_data="metod_21_30")
    button7 = InlineKeyboardButton("31-40 metod", callback_data="metod_31_40")
    button9 = InlineKeyboardButton("41-50 metod", callback_data="metod_41_50")
    button10 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button3, button5, button7, button9, button10)
    return markup

def interaktiv_20btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("1-20 metod", callback_data="metod_1_20")
    button2 = InlineKeyboardButton("21-40 metod", callback_data="metod_21_40")
    button5 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button2, button5)
    return markup

def interaktiv_50btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("1-50 metod", callback_data="metod_1_50")
    button5 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button5)
    return markup





def pedagogik_btns():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Milliy tarbiyaning oiladagi va ta`limdagi roli", callback_data="milliy")
    button2 = InlineKeyboardButton("O`z maqolangizni chop eting", callback_data="maqola")
    button3 = InlineKeyboardButton("Tajribani ommalashtirish", callback_data="tajriba")
    button4 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_kurs")
    markup.add(button1, button2, button3, button4)
    return markup

milliy_price = 10000
maqola_price = 10000
tajriba_price = 10000



def buy():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Xarid qilish", callback_data="buy_cart")
    button2 = InlineKeyboardButton("O‘chirib tashlash", callback_data="clear_cart")
    markup.add(button1, button2)
    return markup

