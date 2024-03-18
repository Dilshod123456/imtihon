from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging
import telebot
from django.http import HttpResponse
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils import timezone
from .models import BotData

TOKEN = '7062908765:AAGgKF--Jw3GR99vy_GakOxXDM6OSUXEDK0'


bot = telebot.TeleBot(TOKEN)


def index(request):
    return HttpResponse("Hello guys")

@csrf_exempt
def bot_view(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode("utf-8"))
        try:
            bot.process_new_updates([update])
        except Exception as e:
            logging.error(e)
        return HttpResponse(status=200)

email_address = 'tuygunovdilshod21@gmail.com'  # Your email address
email_password = 'petr mdak xpvi keml'  # Your email password

# Define the command handler for '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Bu sizning botingiz. Mamlakat maʼlumotlarini elektron pochta orqali olish uchun /mamlakat_malumotlarini_oling <email> dan foydalaning.")

# Define the command handler for '/get_country_info' command
@bot.message_handler(commands=["mamlakat_malumotlarini_oling"])
def get_country_info(message):
    try:
        # Split the message text to get the email address
        command_parts = message.text.split()
        if len(command_parts) != 2:
            bot.reply_to(message, "Yaroqli elektron pochta manzilini kiriting.")
            return

        email = command_parts[1]

        # Get the country code from the message text
        country_code = 'uz'  # Change this to the desired country code
        country_info = fetch_country_info(country_code)

        if country_info:
            send_email(email, country_info)
            bot.reply_to(message, f"Mamlakat ma'lumotlari yuborildi: {email}.")
        else:
            bot.reply_to(message, "Mamlakat ma’lumotlarini olib bo‘lmadi.")
    except Exception as e:
        bot.reply_to(message, "So‘rovni qayta ishlashda xatolik yuz berdi. Iltimos keyinroq qayta urinib ko'ring.")

# Function to fetch country information from REST Countries API
def fetch_country_info(country_code):
    try:
        response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
        data = response.json()

        if data:
            country_name = data[0]['name']['common']
            capital = data[0]['capital']
            population = data[0]['population']
            languages = ', '.join(data[0]['languages'])
            return f"Davlat: {country_name}\nPoytaxt: {capital}\nAholi soni: {population}\nTil: {languages}"
        else:
            return None
    except Exception as e:
        print(f"Error fetching country information: {e}")
        return None

# Function to send email
def send_email(to_email, content):
    try:
        smtp_server = 'smtp.gmail.com'  # Change if using a different email provider
        port = 587  # Gmail SMTP port

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(email_address, email_password)

        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to_email
        msg['Subject'] = 'Country Information'

        body = MIMEText(content, 'plain')
        msg.attach(body)

        server.sendmail(email_address, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def save_to_database(email, country_info):
    BotData.objects.create(timestamp=timezone.now(), country_info=country_info, recipient_email=email)
