import telebot
import zipfile, rarfile, tarfile
import shutil, os, time

# 🔑 BOT TOKEN (BotFather se mila hua)
TOKEN = "8526182224:AAGhSSt1wLc22601WynJdTQiIRP3WoRh6O8"
bot = telebot.TeleBot(TOKEN)

# 🔒 FORCE JOIN CHANNEL
FORCE_CHANNEL = "@Ninjabot_update"

# ✅ Allowed archive formats
ALLOWED = (
    ".zip", ".rar", ".7z",
    ".tar", ".tar.gz", ".tgz",
    ".tar.bz2", ".tar.xz", ".gz"
)

# 🔒 Check user joined channel or not
def is_joined(user_id):
    try:
        status = bot.get_chat_member(FORCE_CHANNEL, user_id).status
        return status in ["member", "administrator", "creator"]
    except:
        return False

# 📂 When user sends a file
@bot.message_handler(content_types=['document'])
def handle_file(message):

    # 🔐 Force join check
    if not is_joined(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "🔔 **JOIN REQUIRED**\n\n"
            "👉 Pehle hamara channel join karein:\n"
            "https://t.me/Ninjabot_update\n\n"
            "⚠️ Join karne ke baad file dobara bhejein.\n\n"
            "Ńíń𝗷á_Ő𝗳𝗳íćíáĺ 🩶🖤🗯",
            disable_web_page_preview=True
        )
        return

    # 📄 File name
    file_name = message.document.file_name.lower()

    # ❌ Wrong file type
    if not file_name.endswith(ALLOWED):
        bot.send_message(
            message.chat.id,
            "⚠️ Pʟᴇᴀꜱᴇ Sᴇɴᴅ A Vᴀʟɪᴅ Aʀᴄʜɪᴠᴇ Fɪʟᴇ.\n\n"
            "ZIP, RAR, 7Z, TAR, TAR.GZ, TGZ, TAR.BZ2, TAR.XZ, GZ\n\n"
            "Ńíń𝗷á_Ő𝗳𝗳íćíáĺ 🩶"
        )
        return

    start = time.time()

    # ⬇️ Download file from Telegram
    file_info = bot.get_file(message.document.file_id)
    file_data = bot.download_file(file_info.file_path)

    # 📁 Create folders
    os.makedirs("work/extracted", exist_ok=True)
    file_path = f"work/{file_name}"

    # 💾 Save file
    with open(file_path, "wb") as f:
        f.write(file_data)

    try:
        # 📦 Extract archive
        if file_name.endswith(".zip"):
            zipfile.ZipFile(file_path).extractall("work/extracted")

        elif file_name.endswith(".rar"):
            rarfile.RarFile(file_path).extractall("work/extracted")

        elif file_name.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")):
            tarfile.open(file_path).extractall("work/extracted")

        # 🔁 Re-zip extracted files
        shutil.make_archive(
            "
