import os
from flask import Flask, request, jsonify
import mysql.connector
from redis import Redis
import ast
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

REDIS_PORT = int(os.getenv("REDIS_PORT") or 6379)
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_DB = int(os.getenv("REDIS_DB") or 0)

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=int(os.getenv("MYSQL_PORT") or 3306),
        database=os.getenv("MYSQL_DB")
    )


@app.route("/")
def hello():
    return "<h1><p>UFRB SA.</p></h1>"


@app.route('/customers', methods=['GET'])
def list_customers():
    name = request.args.get('name')
    address = request.args.get('address')
    query = "SELECT * FROM clientes WHERE 1=1"
    params = []
    if name:
        query += " AND Nome LIKE %s"
        params.append("%{name}%")
    if address:
        query += " AND Endereco LIKE %s"
        params.append(f"%{address}%")

    cache = redis.get(str(params))
    if(cache):
        payload=cache.decode('utf-8')
        return jsonify(ast.literal_eval(payload))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    redis.set(str(params),str(customers))
    return jsonify(customers)


@app.route('/card/<int:card_id>/limit', methods=['GET'])
def get_limit(card_id):
    query = "SELECT Limite FROM cartoes WHERE CartaoID = %s"
    params = (card_id,)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "Card not found"}), 404


@app.route('/card/<int:card_id>/transactions', methods=['GET'])
def list_transactions(card_id):
    query = """
    SELECT t.*
    FROM transacoes t
    WHERE t.CartaoID = %s AND  MONTH(t.DataTransacao) = MONTH(now())
    """
    params = (card_id,)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(transactions)


if __name__ == '__main__':
    app.run(debug=True)
