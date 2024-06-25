import os
from dotenv import load_dotenv
from mysql.connector import connect

load_dotenv()

MYSQL_PORT = int(os.getenv("MYSQL_PORT") or 3306)
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

try:
    connection = connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
    )
    print(connection)
except Exception as e:
    print(f"Error: {e}")
