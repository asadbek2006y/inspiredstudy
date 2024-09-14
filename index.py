#!/usr/bin/python

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Initialize bot with your token
bot = AsyncTeleBot('7529384518:AAGLjBJRrrB5wmb-LDS9p0CWwZbaEZVOuNI')

# Dictionary to collect user data step by step
user_data = {}

# Define the chat ID where you want to send the data
TARGET_CHAT_ID = -4520570706  # Replace with your target chat ID

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('careful-emitter-391618-5ec449ef34dd.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1m4s8bVAg0kije5JmOqF-SLyOqc5y7XVFUz1KMTbYu4Y').sheet1  # Open the spreadsheet by ID and select the first sheet

# Function to send collected data to the target chat
async def send_to_target_chat(message_text):
    try:
        await bot.send_message(TARGET_CHAT_ID, message_text)
    except Exception as e:
        print(f"Failed to send message: {e}")

# Function to save collected data to Google Sheets
async def save_to_google_sheets(data):
    try:
        sheet.append_row([
            data.get('username', 'N/A'),
            data.get('name', 'N/A'),
            data.get('dob', 'N/A'),
            data.get('phone', 'N/A'),
            data.get('residence', 'N/A'),
            data.get('visa', 'N/A'),
            data.get('course', 'N/A'),
            data.get('education_status', 'N/A'),
            data.get('certificate', 'N/A'),
            data.get('certificate_level', 'N/A'),
            data.get('university_name', 'N/A')
        ])
    except Exception as e:
        print(f"Failed to save data to Google Sheets: {e}")

# Command handler for starting the registration process
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    register_button = KeyboardButton('Register')
    markup.add(register_button)
    text = 'Salom, ma\'lumotlarni yig\'ish uchun "Ro\'yxatdan o\'tish" tugmasini bosing.'
    await bot.reply_to(message, text, reply_markup=markup)

# Register button handler
@bot.message_handler(func=lambda message: message.text == 'Register')
async def handle_register(message):
    user_data[message.from_user.id] = {'step': 'get_name', 'username': message.from_user.username}
    await bot.reply_to(message, "Ismingizni kiriting:")

# Collect user data step by step
@bot.message_handler(func=lambda message: message.from_user.id in user_data)
async def collect_data(message):
    user_id = message.from_user.id
    step = user_data[user_id].get('step')

    if step == 'get_name':
        user_data[user_id]['name'] = message.text
        user_data[user_id]['step'] = 'get_dob'
        await bot.reply_to(message, "Tug'ilgan sanangizni kiriting (YYYY-MM-DD):")

    elif step == 'get_dob':
        user_data[user_id]['dob'] = message.text
        user_data[user_id]['step'] = 'get_phone'
        await bot.reply_to(message, "Telefon raqamingizni kiriting:")

    elif step == 'get_phone':
        user_data[user_id]['phone'] = message.text
        user_data[user_id]['step'] = 'get_residence'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Uzbekiston'), KeyboardButton('Chet Elda'))
        await bot.reply_to(message, "Yashash joyingizni tanlang:", reply_markup=markup)

    elif step == 'get_residence':
        user_data[user_id]['residence'] = message.text
        user_data[user_id]['step'] = 'get_visa'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('D4'), KeyboardButton('D2'))
        await bot.reply_to(message, "Viza turini tanlang:", reply_markup=markup)

    elif step == 'get_visa':
        user_data[user_id]['visa'] = message.text
        user_data[user_id]['step'] = 'get_course'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Bakalavr'), KeyboardButton('Magister'))
        await bot.reply_to(message, "Kurs turini tanlang:", reply_markup=markup)

    elif step == 'get_course':
        user_data[user_id]['course'] = message.text
        user_data[user_id]['step'] = 'get_education_status'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Universitetni bitirdim'), KeyboardButton('Universitetni bitirmadim'),
                   KeyboardButton('Maktabni bitirdim'), KeyboardButton('Maktabni bitirmadim'))
        await bot.reply_to(message, "Ta'lim holatini tanlang:", reply_markup=markup)

    elif step == 'get_education_status':
        user_data[user_id]['education_status'] = message.text
        if message.text == 'Universitetni bitirmadim':
            user_data[user_id]['step'] = 'get_university_course'
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('1-kurs'), KeyboardButton('2-kurs'), KeyboardButton('3-kurs'), KeyboardButton('4-kurs'))
            await bot.reply_to(message, "Kursingizni tanlang:", reply_markup=markup)
        elif message.text == 'Maktabni bitirmadim':
            user_data[user_id]['step'] = 'get_school_grade'
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('9-sinf'), KeyboardButton('10-sinf'), KeyboardButton('11-sinf'))
            await bot.reply_to(message, "Sinfingizni tanlang:", reply_markup=markup)
        else:
            user_data[user_id]['education_status'] = 'Universitetni bitirgan' if message.text == 'Universitetni bitirdim' else 'Maktabni bitirgan'
            user_data[user_id]['step'] = 'get_certificate'
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('IELTS'), KeyboardButton('TOPIK'), KeyboardButton('Duolingo'), KeyboardButton('Yo\'q'))
            await bot.reply_to(message, "Sertifikat turini tanlang:", reply_markup=markup)

    elif step == 'get_university_course':
        user_data[user_id]['education_status'] = message.text
        user_data[user_id]['step'] = 'get_certificate'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('IELTS'), KeyboardButton('TOPIK'), KeyboardButton('Duolingo'), KeyboardButton('Yo\'q'))
        await bot.reply_to(message, "Sertifikat turini tanlang:", reply_markup=markup)

    elif step == 'get_school_grade':
        user_data[user_id]['education_status'] = message.text
        user_data[user_id]['step'] = 'get_certificate'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('IELTS'), KeyboardButton('TOPIK'), KeyboardButton('Duolingo'), KeyboardButton('Yo\'q'))
        await bot.reply_to(message, "Sertifikat turini tanlang:", reply_markup=markup)

    elif step == 'get_certificate':
        user_data[user_id]['certificate'] = message.text
        if message.text != 'Yo\'q':
            user_data[user_id]['step'] = 'get_certificate_level'
            await bot.reply_to(message, "Sertifikat darajasini kiriting:")
        else:
            user_data[user_id]['certificate_level'] = 'N/A'
            user_data[user_id]['step'] = 'get_university'
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton('Ha'), KeyboardButton('Yo\'q'))
            await bot.reply_to(message, "Universitetni tanlaganmisiz?", reply_markup=markup)

    elif step == 'get_certificate_level':
        user_data[user_id]['certificate_level'] = message.text
        user_data[user_id]['step'] = 'get_university'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Ha'), KeyboardButton('Yo\'q'))
        await bot.reply_to(message, "Universitetni tanlaganmisiz?", reply_markup=markup)

    elif step == 'get_university':
        if message.text == 'Ha':
            user_data[user_id]['step'] = 'get_university_name'
            await bot.reply_to(message, "Universitet nomini kiriting:")
        else:
            user_data[user_id]['university_name'] = 'Yo\'q'
            await bot.reply_to(message, "Ma'lumotlaringiz saqlanmoqda...")
            await save_to_google_sheets(user_data[user_id])
            await send_to_target_chat(str(user_data[user_id]))
            del user_data[user_id]
            await bot.reply_to(message, "Ma'lumotlaringiz saqlandi!")

    elif step == 'get_university_name':
        user_data[user_id]['university_name'] = message.text
        await bot.reply_to(message, "Ma'lumotlaringiz saqlanmoqda...")
        await save_to_google_sheets(user_data[user_id])
        await send_to_target_chat(str(user_data[user_id]))
        del user_data[user_id]
        await bot.reply_to(message, "Ma'lumotlaringiz saqlandi!")

# Polling loop
async def main():
    while True:
        try:
            await bot.polling(non_stop=True)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
