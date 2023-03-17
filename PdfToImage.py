import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from io import BytesIO
import PyPDF2
from wand.image import Image

# Define the bot token and create a Telegram bot instance
TOKEN = 'your_bot_token_here'
bot = telegram.Bot(token=TOKEN)

# Define the command handler function
def pdf_to_image(update, context):
    # Get the PDF file sent by the user
    file = context.bot.get_file(update.message.document.file_id)
    # Convert the file to a byte stream
    file_stream = BytesIO(file.download_as_bytearray())
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(file_stream)
    # Get the first page of the PDF
    pdf_page = pdf_reader.getPage(0)
    # Create a Wand image object from the PDF page
    with Image(file=pdf_page) as img:
        # Convert the image to JPEG format
        img.format = 'jpeg'
        # Save the image to a byte stream
        img_stream = BytesIO()
        img.save(img_stream)
        # Send the image to the user
        update.message.reply_photo(photo=img_stream)

# Define the main function to start the bot
def main():
    # Create an updater and dispatcher for the bot
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # Define the command handler for the /pdf command
    pdf_handler = MessageHandler(Filters.document.mime_type('application/pdf'), pdf_to_image)
    dispatcher.add_handler(pdf_handler)
    # Start the bot
    updater.start_polling()
    updater.idle()

# Call the main function to start the bot
if __name__ == '__main__':
    main()
