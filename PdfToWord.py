import os
import tempfile
import telebot
import requests


# Replace with your own Telegram bot token
TOKEN = 'your-telegram-bot-token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Check if the received file is a PDF
    if message.document.mime_type == 'application/pdf':
        # Download the file
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Convert the PDF file to Word using the CloudConvert API
        cloudconvert_api_key = 'your-cloudconvert-api-key'
        cloudconvert_url = 'https://api.cloudconvert.com/v2/pdf/to/docx'
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(downloaded_file)
            temp_file.flush()
            with open(temp_file.name, 'rb') as input_file:
                headers = {
                    'Authorization': f'Bearer {cloudconvert_api_key}',
                }
                files = {
                    'file': input_file,
                }
                response = requests.post(cloudconvert_url, headers=headers, files=files)
                response.raise_for_status()
                output_file = response.content
            
            # Send the converted file back to the user
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_output_file:
                temp_output_file.write(output_file)
                temp_output_file.flush()
                with open(temp_output_file.name, 'rb') as docx_file:
                    bot.send_document(message.chat.id, docx_file)

        # Delete the temporary files
        os.unlink(temp_file.name)
        os.unlink(temp_output_file.name)


if __name__ == '__main__':
    bot.polling()
