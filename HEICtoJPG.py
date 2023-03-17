import os
import tempfile
import subprocess
import telebot


# Replace with your own Telegram bot token
TOKEN = 'your-telegram-bot-token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Check if the received file is a HEIC image
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    if file_path.endswith('.HEIC'):
        # Download the HEIC image
        downloaded_file = bot.download_file(file_path)

        # Convert the HEIC image to JPG using the sips command-line tool
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(downloaded_file)
            temp_file.flush()
            subprocess.run(['sips', '-s', 'format', 'jpeg', temp_file.name, '--out', temp_file.name + '.jpg'], check=True)

            # Send the converted image back to the user
            with open(temp_file.name + '.jpg', 'rb') as jpg_file:
                bot.send_photo(message.chat.id, jpg_file)

        # Delete the temporary files
        os.unlink(temp_file.name)
        os.unlink(temp_file.name + '.jpg')


if __name__ == '__main__':
    bot.polling()
