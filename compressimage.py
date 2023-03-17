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

    # Compress the photo using the ImageMagick command-line tool
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(downloaded_file)
        temp_file.flush()
        subprocess.run(['convert', temp_file.name, '-quality', '50%', temp_file.name], check=True)

        # Send the compressed photo back to the user
        with open(temp_file.name, 'rb') as compressed_file:
            bot.send_photo(message.chat.id, compressed_file)

    # Delete the temporary file
    os.unlink(temp_file.name)


if __name__ == '__main__':
    bot.polling()
