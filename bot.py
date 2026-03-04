import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import httpx
from config import TELEGRAM_TOKEN, SHEERID_API_URL, SHEERID_PROGRAM_ID, MILITARY_BRANCHES
from database import init_db, save_user, update_user_status, save_verification_data, get_user, mark_verified

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Conversation states
(START, FULL_NAME, BIRTH_DATE, EMAIL, BRANCH, DISCHARGE_DATE, CONFIRM, VERIFY) = range(8)

# Keyboard layouts
def get_branch_keyboard():
    keyboard = []
    branches = list(MILITARY_BRANCHES.values())
    for i in range(0, len(branches), 2):
        row = [KeyboardButton(branches[i])]
        if i + 1 < len(branches):
            row.append(branches[i + 1])
        keyboard.append(row)
    keyboard.append([KeyboardButton("Cancel")])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username, user.first_name)
    update_user_status(user.id, 'started')

    await update.message.reply_text(
        "🪖 *Veteran Verification Bot*\n\n"
        "Chào mừng! Bot này giúp bạn verify thông tin veteran để nhận ưu đãi từ ChatGPT.\n\n"
        "⚠️ *Lưu ý*: Bạn cần cung cấp thông tin THẬT để verify qua SheerID.\n\n"
        "Bắt đầu bằng cách nhập họ và tên đầy đủ của bạn:",
        parse_mode='Markdown'
    )
    return FULL_NAME

async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_name = update.message.text.strip()
    if len(full_name) < 3:
        await update.message.reply_text("Vui lòng nhập họ và tên đầy đủ:")
        return FULL_NAME

    save_verification_data(update.effective_user.id, {'full_name': full_name, 'status': 'full_name'})
    await update.message.reply_text(
        f"✅ Tên: {full_name}\n\n"
        "Nhập ngày sinh (định dạng YYYY-MM-DD):\n"
        "Ví dụ: 1990-05-15"
    )
    return BIRTH_DATE

async def birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birth_date = update.message.text.strip()

    # Simple date validation
    import re
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date):
        await update.message.reply_text("Định dạng không đúng. Vui lòng nhập YYYY-MM-DD:")
        return BIRTH_DATE

    save_verification_data(update.effective_user.id, {'birth_date': birth_date, 'status': 'birth_date'})
    await update.message.reply_text(
        f"✅ Ngày sinh: {birth_date}\n\n"
        "Nhập địa chỉ email của bạn:"
    )
    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()

    import re
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        await update.message.reply_text("Email không hợp lệ. Vui lòng nhập lại:")
        return EMAIL

    save_verification_data(update.effective_user.id, {'email': email, 'status': 'email'})
    await update.message.reply_text(
        f"✅ Email: {email}\n\n"
        "Chọn quân binh chủng (branch):",
        reply_markup=get_branch_keyboard()
    )
    return BRANCH

async def branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    branch = update.message.text.strip()

    if branch == "Cancel":
        await update.message.reply_text("Đã hủy. Gõ /start để bắt đầu lại.")
        return ConversationHandler.END

    # Convert branch name to code
    branch_code = None
    for code, name in MILITARY_BRANCHES.items():
        if name.lower() == branch.lower():
            branch_code = code
            break

    if not branch_code:
        await update.message.reply_text("Vui lòng chọn từ keyboard:")
        return BRANCH

    save_verification_data(update.effective_user.id, {'branch': branch, 'branch_code': branch_code, 'status': 'branch'})
    await update.message.reply_text(
        f"✅ Quân binh chủng: {branch}\n\n"
        "Nhập ngày xuất ngũ (định dạng YYYY-MM-DD):\n"
        "Ví dụ: 2020-08-20"
    )
    return DISCHARGE_DATE

async def discharge_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    discharge_date = update.message.text.strip()

    import re
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', discharge_date):
        await update.message.reply_text("Định dạng không đúng. Vui lòng nhập YYYY-MM-DD:")
        return DISCHARGE_DATE

    user_data = get_user(update.effective_user.id)
    if user_data:
        full_name = user_data[4]
        birth_date = user_data[5]
        email = user_data[6]
        branch = user_data[7]

        # Find branch code
        branch_code = None
        for code, name in MILITARY_BRANCHES.items():
            if name == branch:
                branch_code = code
                break

        summary = (
            f"📋 *Thông tin xác minh*\n\n"
            f"• Họ tên: {full_name}\n"
            f"• Ngày sinh: {birth_date}\n"
            f"• Email: {email}\n"
            f"• Quân binh chủng: {branch}\n"
            f"• Ngày xuất ngũ: {discharge_date}\n\n"
            f"Thông tin trên có chính xác không?"
        )

        await update.message.reply_text(summary, parse_mode='Markdown',
                                       reply_markup=ReplyKeyboardMarkup(
                                           [["Xác nhận", "Hủy"]], one_time_keyboard=True))
        return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "Hủy":
        await update.message.reply_text("Đã hủy. Gõ /start để bắt đầu lại.")
        return ConversationHandler.END

    if text != "Xác nhận":
        await update.message.reply_text("Vui lòng chọn 'Xác nhận' hoặc 'Hủy':")
        return CONFIRM

    await update.message.reply_text(
        "⏳ Đang khởi tạo verification...\n"
        "Vui lòng đợi..."
    )

    # Create verification on SheerID
    user_data = get_user(update.effective_user.id)
    if not user_data:
        await update.message.reply_text("Lỗi: Không tìm thấy dữ liệu. Gõ /start để bắt đầu lại.")
        return ConversationHandler.END

    full_name, birth_date, email, branch = user_data[4], user_data[5], user_data[6], user_data[7]

    # Find branch code
    branch_code = None
    for code, name in MILITARY_BRANCHES.items():
        if name == branch:
            branch_code = code
            break

    # Create verification
    try:
        async with httpx.AsyncClient() as client:
            # Step 1: Create verification
            create_data = {
                "programId": SHEERID_PROGRAM_ID,
                "metadata": {
                    "firstName": full_name.split()[0],
                    "lastName": " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else "",
                    "birthDate": birth_date,
                    "email": email
                }
            }

            response = await client.post(
                f"{SHEERID_API_URL}/verification/",
                json=create_data,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )

            if response.status_code != 200:
                await update.message.reply_text(
                    f"❌ Lỗi khởi tạo verification: {response.status_code}\n"
                    f"Vui lòng thử lại sau."
                )
                return ConversationHandler.END

            verification_data = response.json()
            verification_id = verification_data.get('verificationId')

            # Step 2: Submit military status
            step1_response = await client.post(
                f"{SHEERID_API_URL}/verification/{verification_id}/step/collectMilitaryStatus",
                json={"status": "VETERAN"},
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )

            if step1_response.status_code != 200:
                await update.message.reply_text(f"❌ Lỗi bước 1: {step1_response.status_code}")
                return ConversationHandler.END

            # Step 3: Submit personal info
            step2_data = {
                "firstName": full_name.split()[0],
                "lastName": " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else "",
                "birthDate": birth_date,
                "email": email,
                "organization": branch_code,
                "dischargeDate": user_data[8] if len(user_data) > 8 else discharge_date,
                "country": "US",
                "locale": "en-US",
                "consent": True
            }

            step2_response = await client.post(
                f"{SHEERID_API_URL}/verification/{verification_id}/step/collectInactiveMilitaryPersonalInfo",
                json=step2_data,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )

            if step2_response.status_code != 200:
                await update.message.reply_text(f"❌ Lỗi bước 2: {step2_response.status_code}\n{step2_response.text}")
                return ConversationHandler.END

            # Save verification ID
            save_verification_data(update.effective_user.id, {
                'verification_id': verification_id,
                'discharge_date': user_data[8] if len(user_data) > 8 else discharge_date,
                'status': 'verifying'
            })

            await update.message.reply_text(
                f"✅ *Verification đã được gửi!*\n\n"
                f"Verification ID: `{verification_id}`\n\n"
                f"Bạn sẽ nhận được email từ SheerID trong vài phút đến vài ngày làm việc.\n\n"
                f"📧 Email: {email}\n\n"
                f"Kiểm tra email để xem kết quả verification.",
                parse_mode='Markdown'
            )

    except Exception as e:
        logger.error(f"Verification error: {e}")
        await update.message.reply_text(
            f"❌ Đã xảy ra lỗi: {str(e)}\n"
            f"Vui lòng thử lại sau."
        )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Đã hủy. Gõ /start để bắt đầu lại.")
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🪖 *Veteran Verification Bot*\n\n"
        "Các lệnh:\n"
        "/start - Bắt đầu verification\n"
        "/status - Kiểm tra trạng thái\n"
        "/help - Trợ giúp\n\n"
        "Bot này giúp verify thông tin veteran qua SheerID để nhận ưu đãi ChatGPT.",
        parse_mode='Markdown'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = get_user(update.effective_user.id)

    if not user_data:
        await update.message.reply_text("Bạn chưa bắt đầu verification. Gõ /start")
        return

    status = user_data[3]
    verified = user_data[9]

    if verified:
        await update.message.reply_text("✅ Bạn đã verified thành công!")
    elif status == 'verifying':
        await update.message.reply_text("⏳ Verification đang được xử lý. Kiểm tra email của bạn.")
    else:
        await update.message.reply_text(f"Trạng thái: {status}. Gõ /start để bắt đầu.")

def main():
    init_db()

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, full_name)],
            BIRTH_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, birth_date)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            BRANCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, branch)],
            DISCHARGE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, discharge_date)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('status', status_command))

    print("Bot đang chạy...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
