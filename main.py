import requests 
import sys
import mysql.connector
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv(dotenv_path='./config/.env')
api_key = os.getenv("api_key")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_port = os.getenv("db_port")

sql_files_path = "./SQL/"

# Connect to database
mydb = mysql.connector.connect(
    host = db_host,
    user = db_user,
    password = db_password
)
cursor = mydb.cursor(buffered=True)

# Functionalities of app

def create_and_use_database():
    # Check if database is present or not
    cursor.execute("SHOW DATABASES;")
    database_present = 0
    for (databases) in cursor:
        if databases[0] == db_name:
            database_present = 1
            break 
    
    # Create database if not present
    if database_present == 0:
        print("Creating Database ", db_name)
        cursor.execute("CREATE DATABASE " + db_name + ";")

    # Use the intended database
    print("Using database ", db_name)
    cursor.execute("USE " + db_name + ";")

def execute_sql_from_file(path, file_name):
    # Read commands from file
    fd = open(path + file_name, 'r')
    sql_file = fd.read()
    fd.close()
    commands = sql_file.split(';')

    for command in commands:
        try:
            print("Executing command: ", command)
            cursor.execute(command)
        except:
            print("Error in executing command: ", command)

def create_schema():
    # Check if desired tables are already present or not
    cursor.execute("SHOW TABLES;")
    genre_table_present = 0
    movies_table_present = 0
    for (tables) in cursor:
        if tables[0] == "genres":
            genre_table_present = 1
        if tables[0] == "movies_table_present":
            movies_table_present = 1

    # Create Genres table if not present
    if genre_table_present == 0:
        print("Creating table for Genres")
        execute_sql_from_file(sql_files_path, "genres.sql")

    # Create Movies table if not present
    if movies_table_present == 0:
        print("Creating table for Movies")
        execute_sql_from_file(sql_files_path, "movies.sql")


def fetch_data_from_api():
    query = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key + "&language=en-US"
    response =  requests.get(query)
    if response.status_code == 200:    # API Hit Successful
        array = response.json()
        return array
    else:                              # API Hit Unsuccessful 
        print("Invalid Request to API")
        sys.exit(1)

def process_data(data):
    pass

def update_database(processed_data):
    pass

# Driver main function
if __name__ == "__main__":
    # Prepare Database
    create_and_use_database()
    create_schema()

    # Fetch data from API and process it
    data = fetch_data_from_api()
    processed_data = process_data(data)

    # Populate the database
    update_database(processed_data)
