# db.py
import psycopg2

DB_CONFIG = {
    "dbname": "Nucleo Diagnostico",
    "user": "postgres",
    "password": "SEBASTIAN18",
    "host": "localhost",
}

def conectar_db():
    return psycopg2.connect(**DB_CONFIG)