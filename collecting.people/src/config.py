import dotenv
import os

dotenv.load_dotenv()

KZN_URL: str  =  os.getenv("KZN_URL", "")
