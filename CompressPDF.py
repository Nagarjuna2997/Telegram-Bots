import os
import tempfile
import telebot
from PyPDF2 import PdfFileReader, PdfFileWriter


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

        # Compress the PDF file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(downloaded_file)
            temp_file.flush()
            with open(temp_file.name, 'rb') as input_file:
                pdf_reader = PdfFileReader(input_file)
                pdf_writer = PdfFileWriter()
                for i in range(pdf_reader.getNumPages()):
                    pdf_writer.addPage(pdf_reader.getPage(i))
                # Set the compression level to 50%
                pdf_writer.setCompressionOptions(compressContentStreams=True, compressionLevel=5)
                with open(temp_file.name, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            # Send the compressed file back to the user
            with open(temp_file.name, 'rb') as compressed_file:
                bot.send_document(message.chat.id, compressed_file)

        # Delete the temporary file
        os.unlink(temp_file.name)


if __name__ == '__main__':
    bot.polling()
