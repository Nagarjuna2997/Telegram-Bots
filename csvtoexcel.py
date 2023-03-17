import os
import csv
import openpyxl
import tempfile
import telebot


# Replace with your own Telegram bot token
TOKEN = 'your-telegram-bot-token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Check if the received file is a CSV file
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    file_name = message.document.file_name
    file_extension = os.path.splitext(file_name)[-1]
    if file_extension.lower() == '.csv':
        # Download the CSV file
        downloaded_file = bot.download_file(file_info.file_path)

        # Convert the CSV file to Excel format
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Create a new Excel workbook
            workbook = openpyxl.Workbook()
            sheet = workbook.active

            # Read the CSV file and write the data to the Excel sheet
            csv_reader = csv.reader(downloaded_file.decode('utf-8').splitlines())
            for row in csv_reader:
                sheet.append(row)

            # Save the Excel workbook to a temporary file
            workbook.save(temp_file.name)

            # Send the Excel file back to the user
            with open(temp_file.name, 'rb') as excel_file:
                bot.send_document(message.chat.id, excel_file, filename=file_name.replace('.csv', '.xlsx'))

        # Delete the temporary files
        os.unlink(temp_file.name)


if __name__ == '__main__':
    bot.polling()
