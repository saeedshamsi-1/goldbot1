import asyncio
from telethon import TelegramClient, events
import re

# اطلاعات لازم برای اتصال به تلگرام
api_id = '2040' 
api_hash = 'b18441a1ff607e10a989891a5462e627'  
phone_number = '989222882031'  
session_name = 'my_session'

# ایجاد کلاینت تلگرام
client = TelegramClient(session_name, api_id, api_hash)

# آیدی کانال‌ها
SOURCE_CHANNEL = '@gooldin1'  # کانال مبدا (آیدی عددی)
DEST_CHANNEL = '@gooldin'  # کانال مقصد (آیدی عددی)

# آیدی قدیمی و جدید که می‌خواهیم جایگزین کنیم
OLD_GROUP_ID = "@aa"
NEW_GROUP_ID = "@saeed"

async def main():
    # اتصال به تلگرام با شماره تلفن
    await client.start(phone_number)

    print("بات با موفقیت متصل شد.")

    # نظارت بر پیام‌های جدید در کانال مبدا
    @client.on(events.NewMessage(chats=SOURCE_CHANNEL))
    async def forward_and_edit(event):
        print("✅ پیام جدید دریافت شد!")

        message = event.message
        if message.text:
            # جایگزینی آیدی قدیمی با آیدی جدید
            new_text = re.sub(re.escape(OLD_GROUP_ID) + r'\s*$', NEW_GROUP_ID, message.text.strip())
            await client.send_message(DEST_CHANNEL, new_text)  # ارسال پیام به کانال مقصد

        elif message.media:
            # پردازش رسانه‌ها (عکس، ویدیو و...)
            caption = message.text if message.text else ""
            new_caption = re.sub(re.escape(OLD_GROUP_ID) + r'\s*$', NEW_GROUP_ID, caption.strip()) if caption else None
            await client.send_file(DEST_CHANNEL, message.media, caption=new_caption)  # ارسال رسانه به کانال مقصد

    # اجرای بی‌نهایت بات تا زمانی که اتصال قطع شود
    await client.run_until_disconnected()

# اجرای کلاینت
loop = asyncio.get_event_loop()
from keep_alive import keep_alive 
loop.run_until_complete(main())
