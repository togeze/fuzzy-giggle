from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))
CATEGORY_TYPES = list(map(str, os.getenv("CATEGORY_TYPES", "").split(",")))
IMAGES_PATH = os.getenv("IMAGES_PATH")
CSV_PATH = os.getenv("CSV_PATH")
MAX_ATTEMPTS= int(os.getenv("MAX_ATTEMPTS"))
