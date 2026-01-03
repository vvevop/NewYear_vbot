[🇷🇺 Русская версия](https://github.com/vvevop/NewYear_vbot/blob/main/README_ru.md)

# 🎄 New Year vbot

![Version](https://img.shields.io/badge/Version-v1.1.1-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet) ![License](https://img.shields.io/badge/License-MIT-green)

A Telegram bot that shows the exact time remaining until the New Year. The bot supports correct word declension (days, hours, minutes) and works in **inline mode** for use in any chat.

## ✨ Features

*   **⏱ Countdown Timer:** Shows days, hours, minutes, and seconds until January 1st of the next year.
*   **💬 Inline Mode:** The bot can be called in any chat (by typing `@username`) to send a beautiful timer to friends.
*   **📚 Grammar:** Uses the `pymorphy3` library for correct Russian word declension (e.g., "1 день", "2 дня", "5 дней").
*   **🛡 Security:** Secure token storage and protected admin functions.

## 🛠 Tech Stack

*   **Python 3.8+**
*   **aiogram 3.x** — Modern asynchronous framework.
*   **python-dotenv** — Environment variable management.
*   **pymorphy3** — Morphological analysis.

## 🚀 Installation and Setup

### 1. Clone the repository
Clone the repository or download the archive:
```bash
git clone https://github.com/vvevop/NewYear_vbot.git
cd NewYear_vbot
```

### Create a virtual environment (Recommended)

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration (.env)

The project uses a .env file to protect secret data.

1. Rename `.env.example` to `.env`.
2. Fill it with your data:

```Ini
BOT_TOKEN=123456789:AAHE...   # Your token from @BotFather

ADMIN_IDS=123456789,987654321 # List of Admin IDs (integers)

MY_ID=123456789               # Your ID for logs (integer)
```

💡 **Tip:** You can find out your ID via the [`@userinfobot`](https://t.me/userinfobot).

### 5. Setup in @BotFather (Important!)

For inline mode to work:

1. Open [@BotFather](https://t.me/botfather).
2. Send the `/mybots` command and select your bot.
3. Go to **Bot Settings** -> **Inline Mode** -> **Turn on**.

### 6. Run

```bash
python3 main.py
```

## 🤖 How to Use

### Private Messages

Send `/start` to the bot to get the timer.

### Inline Mode (in any chat)

1. Type the bot's username in the input field of any chat:
`@username_бота` (don't forget the space at the end!)
2. Click on the tooltip that appears to send the timer.

## 📂 Project Structure

```text
📂 NewYear_vbot
├── ⚙️ .env             # (Created by you!) Stores secret tokens
├── ⚙️ .env.example     # Template to copy from
├── ⚙️ config.py        # Variable loading
├── 🐍 main.py          # Entry point
├── 📄 requirements.txt # Libraries
└── 📝 README.md        # Documentation
```

## 👤 Author

Developer: [@beaitch](https://t.me/beaitch)