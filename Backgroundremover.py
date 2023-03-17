import os
import requests
import telebot


# Replace with your own Telegram bot token
TOKEN = 'your-telegram-bot-token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Download the photo
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Remove the background using the remove.bg API
    removebg_api_key = 'your-removebg-api-key'
    removebg_url = 'https://api.remove.bg/v1.0/removebg'
    headers = {
        'X-Api-Key': removebg_api_key,
    }
    files = {
        'image_file': downloaded_file,
    }
    response = requests.post(removebg_url, headers=headers, files=files)
    response.raise_for_status()
    output_file = response.content
    
    # Send the resulting image back to the user
    with open('output.png', 'wb') as output_image_file:
        output_image_file.write(output_file)
    with open('output.png', 'rb') as output_image_file:
        bot.send_photo(message.chat.id, output_image_file)

    # Delete the temporary files
    os.unlink('output.png')


if __name__ == '__main__':
    bot.polling()
