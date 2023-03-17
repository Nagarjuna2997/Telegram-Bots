import os
import tempfile
import pandas as pd
import telebot


# Replace with your own Telegram bot token
TOKEN = 'your-telegram-bot-token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Download the document
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Save the document to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(downloaded_file)
        temp_file.flush()

        # Read the Excel file into a DataFrame
        excel_data = pd.read_excel(temp_file.name, sheet_name=None)

        # Split the Excel file into multiple sheets and send each sheet back to the user
        for sheet_name, sheet_data in excel_data.items():
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as sheet_file:
                # Save the sheet to a temporary file
                sheet_data.to_excel(sheet_file.name, index=False)

                # Send the sheet back to the user
                with open(sheet_file.name, 'rb') as sheet_data_file:
                    bot.send_document(message.chat.id, sheet_data_file)

            # Delete the temporary sheet file
            os.unlink(sheet_file.name)

    # Delete the temporary file
    os.unlink(temp_file.name)


if __name__ == '__main__':
    bot.polling()
