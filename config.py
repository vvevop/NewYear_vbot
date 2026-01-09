import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

HEARTBEAT_URL = os.getenv("HEARTBEAT_URL")

admin_ids_str = os.getenv("ADMIN_IDS")
if admin_ids_str:
    ADMIN_IDS = [int(id_str) for id_str in admin_ids_str.split(",")]
else:
    ADMIN_IDS = []

my_id_str = os.getenv("MY_ID")
MY_ID = int(my_id_str) if my_id_str else None

BOT_VERSION = "1.1.1"

if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не установлена в файле .env!")