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
    markup = InlineKeyboardMarkup(row_width=1)
    buy_button = InlineKeyboardButton("Ushbu kitobni sotib olish", callback_data="buy_book")
    button5 = InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_to_main")
    markup.add(buy_button, button5)
    return markup

def kitob_delivery():
    markup = InlineKeyboardMarkup(row_width=1)
    yandex_button = InlineKeyboardButton("Yandex Доставка(Toshkent bo‘ylab)", callback_data="yandex_delivery")
    bts_button = InlineKeyboardButton("BTS Доставка(viloyatlar bo‘yicha)", callback_data="bts_delivery")
    button5 = InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_to_main")
    markup.add(yandex_button, bts_button, button5)
    return markup

def payment():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Click", url="https://indoor.click.uz/pay?id=054236&t=0&amount=10000")
    button2 = InlineKeyboardButton("Payme", url="https://payme.uz/fallback/merchant/?id=65200f1f5a8224b99c9a37e3")
    button3 = InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_to_main")
    markup.add(button1, button2, button3)
    return markup

#---------------kurs-------------------
def kurs_btns():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Samarali interaktiv metodlar", callback_data="menu_interaktiv")
    button2 = InlineKeyboardButton("Pedagogik kurslar", callback_data="menu_pedagogik")
    button3 = InlineKeyboardButton("Ekspertlar uchun metodologik xizmat", callback_data="kurs_ekspert")
    button4 = InlineKeyboardButton("Shogirtlar uchun metodologik kurs", callback_data="kurs_shogirt")
    button5 = InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_to_main")
    markup.add(button1, button2, button3, button4, button5)
    return markup

def interaktiv_btns():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("5ta metodli mini kurslar", callback_data="interaktiv_5")
    button2 = InlineKeyboardButton("10ta metodli mini kurslar", callback_data="interaktiv_10")
    button3 = InlineKeyboardButton("25ta metodli kurslar", callback_data="interaktiv_20")
    button4 = InlineKeyboardButton("50ta metodli maxi kurslar", callback_data="interaktiv_50")
    button5 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_kurs")
    markup.add(button1, button2, button3, button4, button5)
    return markup

def pedagogik_btns():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Milliy tarbiyaning oiladagi va ta`limdagi roli", callback_data="milliy")
    button2 = InlineKeyboardButton("O`z maqolangizni chop eting", callback_data="maqola")
    button3 = InlineKeyboardButton("Tajribani ommalashtirish", callback_data="tajriba")
    button4 = InlineKeyboardButton("Lider ustoz", callback_data="lider")
    button5 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_kurs")
    markup.add(button1, button2, button3, button4, button5)
    return markup

def buy():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Xarid qilish", callback_data="buy_cart")
    button2 = InlineKeyboardButton("O‘chirib tashlash", callback_data="clear_cart")
    markup.add(button1, button2)
    return markup

def shogirt_ariza():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Ariza yuborish", callback_data="shogirt_ariza_btn")
    button5 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_kurs")
    markup.add(button1, button5)
    return markup

def expert_ariza():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Ariza yuborish", callback_data="expert_ariza_btn")
    button5 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_kurs")
    markup.add(button1, button5)
    return markup

def lider_add_to_cart():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="lider_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="menu_pedagogik")
    markup.add(button1, button2)
    return markup

def milliy_add_to_cart():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="milliy_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="menu_pedagogik")
    markup.add(button1, button2)
    return markup

def maqola_add_to_cart():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="maqola_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="menu_pedagogik")
    markup.add(button1, button2)
    return markup

def tajriba_add_to_cart():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="tajriba_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="menu_pedagogik")
    markup.add(button1, button2)
    return markup

def interaktiv_5btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("1chi to‘plam", callback_data="toplam1")
    button2 = InlineKeyboardButton("2chi to‘plam", callback_data="toplam2")
    button3 = InlineKeyboardButton("3chi to‘plam", callback_data="toplam3")
    button4 = InlineKeyboardButton("4chi to‘plam", callback_data="toplam4")
    button5 = InlineKeyboardButton("5chi to‘plam", callback_data="toplam5")
    button6 = InlineKeyboardButton("6chi to‘plam", callback_data="toplam6")
    button7 = InlineKeyboardButton("7chi to‘plam", callback_data="toplam7")
    button8 = InlineKeyboardButton("8chi to‘plam", callback_data="toplam8")
    button9 = InlineKeyboardButton("9chi to‘plam", callback_data="toplam9")
    button10 = InlineKeyboardButton("10chi to‘plam", callback_data="toplam10")
    button11 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11)
    return markup

def toplam_5ta_btn1():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam1_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn2():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam2_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn3():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam3_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn4():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam4_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn5():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam5_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn6():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam6_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn7():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam7_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn8():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam8_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn9():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam9_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def toplam_5ta_btn10():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam10_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_5")
    markup.add(button1, button2)
    return markup

def interaktiv_10btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("1chi to‘plam", callback_data="toplam1_2")
    button2 = InlineKeyboardButton("2chi to‘plam", callback_data="toplam3_4")
    button3 = InlineKeyboardButton("3chi to‘plam", callback_data="toplam5_6")
    button4 = InlineKeyboardButton("4chi to‘plam", callback_data="toplam7_8")
    button5 = InlineKeyboardButton("5chi to‘plam", callback_data="toplam9_10")
    button11 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button2, button3, button4, button5, button11)
    return markup

def toplam_10ta_btn1():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam10_1_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_10")
    markup.add(button1, button2)
    return markup

def toplam_10ta_btn2():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam10_2_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_10")
    markup.add(button1, button2)
    return markup

def toplam_10ta_btn3():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam10_3_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_10")
    markup.add(button1, button2)
    return markup

def toplam_10ta_btn4():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam10_4_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_10")
    markup.add(button1, button2)
    return markup

def toplam_10ta_btn5():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam10_5_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_10")
    markup.add(button1, button2)
    return markup


def interaktiv_25btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("1 chi to‘plamlar", callback_data="toplam1_25")
    button2 = InlineKeyboardButton("2 chi to‘plamlar", callback_data="toplam26_50")
    button11 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button2, button11)
    return markup

def toplam_25ta_btn1():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam25_1_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_20")
    markup.add(button1, button2)
    return markup

def toplam_25ta_btn2():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam25_2_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_20")
    markup.add(button1, button2)
    return markup


def interaktiv_50btn():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("10ta to‘plamlar", callback_data="toplam1_50")
    button11 = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_int")
    markup.add(button1, button11)
    return markup

def toplam_50ta_btn1():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("🗑️ Savatchaga qoshish", callback_data="toplam50_1_to_cart_btn")
    button2 = InlineKeyboardButton("⬅️ Orqaga", callback_data="interaktiv_50")
    markup.add(button1, button2)
    return markup
