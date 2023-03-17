import telebot
from PIL import Image
import io
import os

TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello, welcome to the Image to PDF bot! Send me an image and I will convert it to PDF.')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    img = Image.open(io.BytesIO(file))
    img.save('temp_image.png', 'PNG')
    pdf_filename = 'File.pdf'
    img.save(pdf_filename, 'PDF', resolution=100.0)
    with open(pdf_filename, 'rb') as f:
        bot.send_document(chat_id, f)
    os.remove('temp_image.png')
    os.remove(pdf_filename)

bot.polling()
