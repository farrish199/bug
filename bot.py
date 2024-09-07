import telebot
from telebot import types
import re

# Token API bot anda
TOKEN = '7409687169:AAGM1ybul2bukhyumgpQy8CBlrxUDeP-ijI'
bot = telebot.TeleBot(TOKEN)

def get_start_keyboard() -> types.ReplyKeyboardMarkup:
    """Sediakan papan kekunci untuk arahan /start."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Bug Vless")
    keyboard.add(start_button)
    return keyboard

def get_bugvless_keyboard() -> types.ReplyKeyboardMarkup:
    """Sediakan papan kekunci untuk arahan Bug Vless."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [
        "Digi BS", "Digi XL", "UmoFunz XL", "Maxis UL",
        "Unifi XL", "Yes XL", "Celcom XL", "Booster 1", "Booster 2"
    ]
    keyboard.add(*buttons)
    return keyboard

@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    """Handle /start command."""
    bot.reply_to(
        message,
        "===================================\nBot MF By IMMANVPN\n\n"
        "Hi! Saya adalah bot yang dapat membantu anda dalam beberapa hal "
        "yang dapat memudahkan kerja anda!\n\nSaya mempunyai beberapa fungsi "
        "menarik yang dapat anda gunakan!\n\nKlik butang di bawah untuk memulakan.\n"
        "===================================",
        reply_markup=get_start_keyboard()  # Papan kekunci utama
    )

@bot.message_handler(func=lambda message: message.text == "Bug Vless")
def handle_bugvless(message: telebot.types.Message):
    """Handle Bug Vless button and show options."""
    bot.reply_to(
        message,
        "Pilih salah satu pilihan di bawah:",
        reply_markup=get_bugvless_keyboard()
    )

def extract_info_from_text(user_text: str) -> tuple:
    """Extract UUID, subdomain, and name from a full vless URL."""
    pattern = r"vless://([^@]+)@([^:]+):(\d+)\?path=/vlessws&encryption=none&type=ws#(.+)"
    match = re.match(pattern, user_text)
    if match:
        uuid = match.group(1)
        subdo = match.group(2)
        name = match.group(4)
        return uuid, subdo, name
    return None, None, None

def handle_conversion(message: telebot.types.Message):
    """Handle conversion options based on user's selected format."""
    user_text = message.text
    uuid, subdo, name = extract_info_from_text(user_text)
    if uuid and subdo and name:
        conversion_options = {
            "Digi BS": f"vless://{uuid}@162.159.134.61:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
            "Digi XL": f"vless://{uuid}@app.optimizely.com:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
            "UmoFunz XL": f"vless://{uuid}@your-address:80?path=/vlessws&encryption=none&type=ws&host=m.pubgmobile.com#{name}",
            "Maxis UL": f"vless://{uuid}@speedtest.net:443?path=/vlessws&encryption=none&type=ws&host=fast.{subdo}&sni=speedtest.net#{name}",
            "Unifi XL": f"vless://{uuid}@104.17.10.12:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
            "Yes XL": f"vless://{uuid}@104.17.113.188:80?path=/vlessws&encryption=none&type=ws&host=tap-database.who.int.{subdo}#{name}",
            "Celcom XL": f"vless://{uuid}@104.17.148.22:80?path=/vlessws&encryption=none&type=ws&host=opensignal.com.{subdo}#{name}",
            "Booster 1": f"vless://{uuid}@104.17.147.22:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
            "Booster 2": f"vless://{uuid}@www.speedtest.net:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}"
        }
        reply = conversion_options.get(message.text, "Invalid option selected.")
        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, "Invalid URL format. Please send a valid vless URL.")

@bot.message_handler(func=lambda message: message.text in [
    "Digi BS", "Digi XL", "UmoFunz XL", "Maxis UL",
    "Unifi XL", "Yes XL", "Celcom XL", "Booster 1", "Booster 2"
])
def handle_option(message: telebot.types.Message):
    """Handle the options selected by user."""
    handle_conversion(message)

# Mulakan bot
bot.polling()
