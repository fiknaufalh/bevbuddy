import json
import mysql.connector
from utils.config import settings

config = {
    'host': settings.db_hostname,
    'user': settings.db_username,
    'password': settings.db_password,
    'database': settings.db_name,
    'ssl_ca': settings.db_sslmode  
}

def insert_data_to_mysql(json_file_path, config, table_name):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()

            count = 1
            for item in data:
                try:
                    columns = ', '.join(item.keys())
                    placeholders = ', '.join(['%s'] * len(item))
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    values = tuple(item.values())

                    print(f"{count}. {query} {values}\n")
                    count += 1

                    cursor.execute(query, values)
                except:
                    continue

            connection.commit()
            print("Data is already saved in: ", table_name)

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    insert_data_to_mysql(r"data/web_scraping/menu.json", config, "menu")
    insert_data_to_mysql(r"data/web_scraping/nutrition.json", config, "nutrition")