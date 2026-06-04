import os
import logging
from gtts import gTTS
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ⚠️ PUT YOUR NEW TTS BOT TOKEN HERE
TOKEN = "YOUR_NEW_TTS_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🗣️ **Welcome to Text-to-Speech Bot!**\n\n"
        "Send me any text message, and I will instantly turn it into a high-quality voice note! 🎧"
    )

async def convert_text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    
    # Ignore command messages
    if user_text.startswith('/'):
        return

    # Send typing status
    status_msg = await update.message.reply_text("🎤 *Generating voice note... please wait.*", parse_mode="Markdown")
    await update.message.reply_chat_action(action="record_voice")
    
    filename = f"voice_{update.message.message_id}.ogg"
    
    try:
        # Generate speech using Google TTS (Default English 'en')
        tts = gTTS(text=user_text, lang='en', slow=False)
        tts.save(filename)
        
        # Send the audio file as a native Telegram voice note
        with open(filename, 'rb') as voice_file:
            await update.message.reply_voice(voice=voice_file, caption="✨ Here is your audio!")
            
        # Delete the temporary status message
        await status_msg.delete()

    except Exception as e:
        logger.error(f"TTS Bot Error: {e}")
        await status_msg.edit_text("❌ Failed to generate audio. Please try again.")
        
    finally:
        # Clean up the audio file from the server memory
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_text_to_speech))
    
    print("✅ TTS Bot is successfully running...")
    application.run_polling(drop_pending_updates=True)
