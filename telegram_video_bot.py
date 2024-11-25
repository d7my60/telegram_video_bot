from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp
import os

# توكن البوت
TOKEN = '7831551453:AAEEAudMdhL4XjkeMgb6C02LxhkSY9tdv-s'

# مسار حفظ الفيديوهات
DOWNLOAD_PATH = 'downloads/'

# الدالة التي تتعامل مع أوامر البداية
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('مرحباً! أرسل لي رابط الفيديو وسأحاول تنزيله.')

# الدالة التي تقوم بتنزيل الفيديو
async def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    try:
        # التحقق من وجود المجلد لحفظ الفيديوهات
        if not os.path.exists(DOWNLOAD_PATH):
            os.makedirs(DOWNLOAD_PATH)

        # إعدادات yt-dlp لتنزيل الفيديو
        ydl_opts = {
            'format': 'best',  # الأفضل من حيث الجودة
            'outtmpl': f'{DOWNLOAD_PATH}%(title)s.%(ext)s',  # مسار حفظ الفيديو
        }

        # تنزيل الفيديو باستخدام yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # تحميل الفيديو
            video_title = info_dict.get('title', None)  # استخراج عنوان الفيديو
            video_filename = f"{video_title}.mp4"  # تعيين اسم الفيديو

        # إرسال الفيديو بعد تحميله
        video_path = os.path.join(DOWNLOAD_PATH, video_filename)
        await update.message.reply_video(open(video_path, 'rb'), caption=f"تم تنزيل الفيديو: {video_title}")

        # بعد إرسال الفيديو، يمكن حذف الفيديو المحمل من جهازك (اختياري)
        os.remove(video_path)

    except Exception as e:
        await update.message.reply_text(f'حدث خطأ أثناء تنزيل الفيديو: {e}')

# إعداد البوت وإضافة معالجات الرسائل
def main():
    # إعداد البوت باستخدام التوكن
    application = Application.builder().token(TOKEN).build()

    # إضافة معالجات للأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
