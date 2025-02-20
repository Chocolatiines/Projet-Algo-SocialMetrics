import mysql.connector
from mysql.connector import Error
import os
import pandas as pd

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "socialmetrics_db"

CSV_FILE = "tweets_data.csv"

try:
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )

    if connection.is_connected():
        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
        print(f"Database {MYSQL_DB} created successfully.")

        connection.database = MYSQL_DB

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                text TEXT NOT NULL,
                positive TINYINT(1) NOT NULL CHECK (positive IN (0, 1)),
                negative TINYINT(1) NOT NULL CHECK (negative IN (0, 1))
            )
        """)
        print("Table tweets created successfully.")

        cursor.execute("TRUNCATE TABLE tweets")

        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)

            if {"text", "positive", "negative"}.issubset(df.columns):
                for _, row in df.iterrows():
                    sql = "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)"
                    values = (row["text"], int(row["positive"]), int(row["negative"]))
                    cursor.execute(sql, values)

                connection.commit()
                print("Data inserted successfully.")
            else:
                print("CSV file does not have the required columns.")
        else:
            print("CSV file does not exist.")

        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")