'''

API Key (v3 Auth): ac777706efca4c7b54b9bdb61b2e5f63
API Read Access Token (v4 Auth) : eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYzc3NzcwNmVmY2E0YzdiNTRiOWJkYjYxYjJlNWY2MyIsInN1YiI6IjYzZWNlMDQ3ZjkyNTMyMDBjMzAwMTJlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z58LZVwmGUJbbHXTdfDRsJIhxBCxRhJycNEnbkB1qc8

'''

import requests 
import json
import sys
import mysql.connector
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
api_key = os.getenv("api_key")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_port = os.getenv("db_port")

# Connect to database
mydb = mysql.connector.connect(
    host = db_host,
    user = db_user,
    password = db_password
)
cursor = mydb.cursor()

# Functionalities of app

def fetch_data_from_api():
    query = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key +"&language=en-US"
    response =  requests.get(query)
    if response.status_code == 200:    # API Hit Successful
        array = response.json()
        return array
    else:
        print("Invalid Request to API")
        sys.exit(1)

def process_data(data):
    pass

def update_database(processed_data):
    pass

# Driver main function
if __name__ == "__main__":
    data = fetch_data_from_api()
    print(data)
    processed_data = process_data(data)
    update_database(processed_data)