from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Kanal kullanıcı adı ve bağlantısı
CHANNEL_USERNAME = 'ethancheater'  # Kanal kullanıcı adı
CHANNEL_LINK = 'https://t.me/ethancheater'  # Kanalın tam linki

# Kanal kullanıcı kontrol fonksiyonu
async def is_user_subscribed(context: ContextTypes.DEFAULT_TYPE, user_id: int, channel_username: str) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=f"@{channel_username}", user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Kullanıcıdan kanal üyeliğini kontrol et ve mesaj gönder
async def check_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name: str = None, file_content: str = None):
    user_id = update.effective_user.id

    # Kullanıcının kanala üye olup olmadığını kontrol et
    if not await is_user_subscribed(context, user_id, CHANNEL_USERNAME):
        # Katılma bağlantısını ve kontrol butonunu içeren mesaj
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Kanala Katıl", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ Kontrol Et", callback_data="check_subscription")]
        ])
        await update.message.reply_text(
            "<b>❌ Bu botu kullanabilmek için önce kanala katılmalısınız.</b>\n\n"
            "<b>Katıldıktan sonra aşağıdaki butona tıklayarak kontrol edebilirsiniz.</b>",
            reply_markup=join_button,
            parse_mode="HTML"
        )
        return

    # Kullanıcı üye ise dosyayı gönder veya özel mesaj
    if file_name and file_content:
        with open(file_name, "w") as file:
            file.write(file_content)
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_name, "rb"))
    else:
        await update.message.reply_text("<b>✅ Kanallara zaten katılmışsınız, botu kullanabilirsiniz.</b>", parse_mode="HTML")

# /start komutunu işleyen fonksiyon
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_and_send(update, context)

# /valorant komutunu işleyen fonksiyon
async def send_valorant_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_and_send(update, context, "valorant.txt", "valo1:valo1\nvalo2:valo2\nvalo3:valo3")

# /pubg komutunu işleyen fonksiyon
async def send_pubg_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_and_send(update, context, "pubg.txt", "pubg1:pubg1\npubg2:pubg2\npubg3:pubg3")

# /counter komutunu işleyen fonksiyon
async def send_counter_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_and_send(update, context, "counter.txt", "counter1:counter1\ncounter2:counter2\ncounter3:counter3")

# Kontrol butonuna tıklanınca çalışan fonksiyon
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # Kullanıcının kanala üye olup olmadığını kontrol et
    if await is_user_subscribed(context, user_id, CHANNEL_USERNAME):
        await query.message.edit_text(
            "<b>✅ Kanala katıldığınız için teşekkürler! Botu kullanabilirsiniz.</b>",
            parse_mode="HTML"
        )
    else:
        await query.answer("❌ Hâlâ kanala katılmamışsınız. Lütfen önce kanala katılın.", show_alert=True)

# Botun çalışmasını başlat
def main():
    # Bot Token'i buraya yazın
    TOKEN = "7010313102:AAGUEbgTHuU7toWj7MYJNRDjvrZVeOw2eAE"

    # Application oluştur
    application = Application.builder().token(TOKEN).build()

    # Komutları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("valorant", send_valorant_file))
    application.add_handler(CommandHandler("pubg", send_pubg_file))
    application.add_handler(CommandHandler("counter", send_counter_file))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))

    # Botu çalıştır
    application.run_polling()

if __name__ == "__main__":
    main()