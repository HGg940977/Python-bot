import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from sticker_generator import StickerGenerator

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! I\'m a sticker generator bot. Send me an image to create a sticker!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
    Here's how to use me:
    1. Send me any image
    2. I'll convert it into a proper Telegram sticker format
    3. Send /newpack to create a new sticker pack
    4. Send /addsticker to add a sticker to an existing pack
    
    Note: Images should be clear and simple for the best results!
    """
    await update.message.reply_text(help_text)

async def process_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming images and convert them to stickers."""
    try:
        # Get the largest available photo
        photo = update.message.photo[-1]
        
        # Download the photo
        photo_file = await context.bot.get_file(photo.file_id)
        image_bytes = await photo_file.download_as_bytearray()
        
        # Process the image
        sticker_bytes = StickerGenerator.process_image(image_bytes)
        
        # Send the processed image back
        await update.message.reply_document(
            document=sticker_bytes,
            filename='sticker.png',
            caption='Here\'s your processed sticker! Use /newpack to create a new sticker pack or /addsticker to add to existing pack.'
        )
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        await update.message.reply_text(
            "Sorry, there was an error processing your image. Please try again!"
        )

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, process_image))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
