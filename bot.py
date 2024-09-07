import telebot
from telebot import types
import re

# Token API bot anda
TOKEN = '7409687169:AAGM1ybul2bukhyumgpQy8CBlrxUDeP-ijI'
bot = telebot.TeleBot(TOKEN)

# Simpan status dan pilihan pengguna
user_states = {}

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

def get_cancel_keyboard() -> types.ReplyKeyboardMarkup:
    """Sediakan papan kekunci untuk membatalkan permintaan."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.KeyboardButton("Cancel")
    keyboard.add(cancel_button)
    return keyboard

@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    """Handle /start command."""
    bot.send_message(
        message.chat.id,
        "===================================\nBot MF By IMMANVPN\n\n"
        "Hi! Saya adalah bot yang dapat membantu anda dalam beberapa hal "
        "yang dapat memudahkan kerja anda!\n\nSaya mempunyai beberapa fungsi "
        "menarik yang dapat anda gunakan!\n\nKlik butang di bawah untuk memulakan.\n"
        "===================================",
        reply_markup=get_start_keyboard()
    )

@bot.message_handler(func=lambda message: message.text == "Bug Vless")
def handle_bugvless(message: telebot.types.Message):
    """Handle Bug Vless button and show options."""
    user_states[message.chat.id] = {'state': 'awaiting_vless_url', 'format': None}
    bot.send_message(
        message.chat.id,
        "Pilih salah satu pilihan di bawah:",
        reply_markup=get_bugvless_keyboard()
    )

@bot.message_handler(func=lambda message: message.text in [
    "Digi BS", "Digi XL", "UmoFunz XL", "Maxis UL",
    "Unifi XL", "Yes XL", "Celcom XL", "Booster 1", "Booster 2"
])
def handle_bugvless_option(message: telebot.types.Message):
    """Handle the options selected by user for Bug Vless."""
    if message.chat.id in user_states and user_states[message.chat.id]['state'] == 'awaiting_vless_url':
        selected_option = message.text
        user_states[message.chat.id]['format'] = selected_option
        bot.send_message(
            message.chat.id,
            f"Anda memilih {selected_option}. Sila hantar URL Vless anda:",
            reply_markup=get_cancel_keyboard()
        )

@bot.message_handler(func=lambda message: message.text.startswith("vless://"))
def handle_vless_url(message: telebot.types.Message):
    """Handle the Vless URL sent by the user."""
    if message.chat.id in user_states and user_states[message.chat.id]['state'] == 'awaiting_vless_url':
        selected_format = user_states[message.chat.id].get('format')
        if selected_format:
            # Process the URL with the selected format
            user_text = message.text
            uuid, subdo, name = extract_info_from_text(user_text)
            if uuid and subdo and name:
                conversion_options = {
                    "Digi BS": f"vless://{uuid}@162.159.134.61:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "Digi XL": f"vless://{uuid}@app.optimizely.com:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "UmoFunz XL": f"vless://{uuid}@{subdo}:80?path=/vlessws&encryption=none&type=ws&host=m.pubgmobile.com#{name}",
                    "Maxis UL": f"vless://{uuid}@speedtest.net:443?path=/vlessws&encryption=none&type=ws&host=fast.{subdo}&sni=speedtest.net#{name}",
                    "Unifi XL": f"vless://{uuid}@104.17.10.12:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "Yes XL": f"vless://{uuid}@104.17.113.188:80?path=/vlessws&encryption=none&type=ws&host=tap-database.who.int.{subdo}#{name}",
                    "Celcom XL": f"vless://{uuid}@104.17.148.22:80?path=/vlessws&encryption=none&type=ws&host=opensignal.com.{subdo}#{name}",
                    "Booster 1": f"vless://{uuid}@104.17.147.22:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "Booster 2": f"vless://{uuid}@www.speedtest.net:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}"
                }
                reply = conversion_options.get(selected_format, "Invalid option selected.")
                bot.send_message(message.chat.id, reply)
            else:
                bot.send_message(message.chat.id, "Invalid URL format. Please send a valid vless URL.")
            
            # Reset user state
            user_states[message.chat.id] = {'state': None, 'format': None}

@bot.message_handler(func=lambda message: message.text == "Cancel")
def handle_cancel(message: telebot.types.Message):
    """Handle Cancel button and reset state."""
    if message.chat.id in user_states:
        user_states[message.chat.id] = {'state': None, 'format': None}
        bot.send_message(
            message.chat.id,
            "Permintaan dibatalkan. Sila pilih butang lain jika anda ingin memulakan semula.",
            reply_markup=get_start_keyboard()
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

# Mulakan bot
bot.polling()
