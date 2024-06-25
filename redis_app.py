import os
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

REDIS_PORT = int(os.getenv("REDIS_PORT") or 6379)
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_DB = int(os.getenv("REDIS_DB") or 0)

try:
    connection = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    print(connection)
except Exception as e:
    print(f"Error: {e}")
