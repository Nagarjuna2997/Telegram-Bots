import os
import tempfile
import subprocess
import telebot


# Replace with your own Telegram bot token
TOKEN = 'your-telegram-bot-token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Download the photo
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Convert the photo to JPEG format using the ImageMagick command-line tool
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(downloaded_file)
        temp_file.flush()
        subprocess.run(['convert', temp_file.name, '-quality', '80%', '-background', 'white', '-flatten', temp_file.name + '.jpg'], check=True)

        # Send the converted photo back to the user
        with open(temp_file.name + '.jpg', 'rb') as converted_file:
            bot.send_photo(message.chat.id, converted_file)

    # Delete the temporary files
    os.unlink(temp_file.name)
    os.unlink(temp_file.name + '.jpg')


if __name__ == '__main__':
    bot.polling()
