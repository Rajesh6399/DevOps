import os
import psycopg2
from time import sleep

# Load environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")

# Try connecting to PostgreSQL (wait until ready)
while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Connected to PostgreSQL successfully!")
        break
    except psycopg2.OperationalError:
        print("⏳ Waiting for PostgreSQL to be ready...")
        sleep(2)

cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(100)
    );
""")

# Insert sample record
cur.execute("""
    INSERT INTO users (name, email)
    VALUES ('alice', 'alice@example.com')
    ON CONFLICT DO NOTHING;
""")

# Retrieve and display data
cur.execute("SELECT * FROM users;")
rows = cur.fetchall()

print("📋 Data in 'users' table:")
for row in rows:
    print(row)

conn.commit()
cur.close()
conn.close()
