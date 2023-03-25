import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
GROUPS_ID = str(os.getenv("GROUPS_ID")).split(" ")
DATABASE = str(os.getenv("DATABASE"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
ADMIN = str(os.getenv("ADMIN")).split(" ")
SLEEP_TIME = .3

ip = str(os.getenv("ip"))

