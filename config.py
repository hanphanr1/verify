# Veteran Verification Bot Configuration

# Telegram Bot
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"

# SheerID Configuration
SHEERID_API_URL = "https://services.sheerid.com/rest/v2"
# Program ID for ChatGPT Veterans (cần lấy từ SheerID dashboard)
SHEERID_PROGRAM_ID = "YOUR_PROGRAM_ID"

# Military Branch Codes
MILITARY_BRANCHES = {
    "4070": "Army",
    "4071": "Marine Corps",
    "4072": "Navy",
    "4073": "Air Force",
    "4074": "Coast Guard",
    "4544268": "Space Force"
}

# Database
DB_PATH = "veteran_bot.db"
