import requests 
import sys
import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

# Load Environment Variables
load_dotenv(dotenv_path='./config/.env')

api_key = os.getenv("api_key")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_port = os.getenv("db_port")
sql_files_path = Path("./SQL/")

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
    fd = open(path / file_name, 'r')
    sql_file = fd.read()
    fd.close()
    commands = sql_file.split(';')

    for command in commands:
        try:
            cursor.execute(command)
        except:
            print("Error in executing command: ", command)

def create_schema():
    # Check if desired tables are already present or not
    cursor.execute("SHOW TABLES;")
    genre_table_present = 0
    movies_table_present = 0
    relations_table_present = 0
    for (tables) in cursor:
        if tables[0] == "genres":
            genre_table_present = 1
        if tables[0] == "movies":
            movies_table_present = 1
        if tables[0] == "genre_movie_relation":
            relations_table_present = 1

    # Create Genres table if not present
    if genre_table_present == 0:
        print("Creating table for Genres")
        execute_sql_from_file(sql_files_path, "genres.sql")

    # Create Movies table if not present
    if movies_table_present == 0:
        print("Creating table for Movies")
        execute_sql_from_file(sql_files_path, "movies.sql")

    # Create Genre-Movie relation table if not present
    if relations_table_present == 0:
        print("Creating table for Genre-Movie relation")
        execute_sql_from_file(sql_files_path, "genre_movie_relation.sql")

def update_genres():
    # Fetch all genres from API
    query = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key + "&language=en-US"
    response =  requests.get(query)
    new_genres_array = []
    if response.status_code == 200:    # API Hit Successful
        genres_json = response.json()
        for d in genres_json['genres']:
            new_genres_array.append((d['id'], d['name']))
    else:                              # API Hit Unsuccessful 
        print("Invalid request of genres to API")
        sys.exit(1)
    
    # Fetch all present genres
    cursor.execute("SELECT genre_id FROM genres;")
    current_genres_array = cursor.fetchall()
    current_genres_array = set(current_genres_array)

    # Add new genres to database
    for (genre_id, genre) in new_genres_array:
        if (genre_id,) not in current_genres_array:
            print("Found new genre: ", genre)
            current_genres_array.add((genre_id,))
            command = "INSERT INTO genres VALUES (" + str(genre_id) + ",'" + str(genre) + "');"
            cursor.execute(command)

    # Commit changes to database
    mydb.commit()

    return current_genres_array

def update_movies(genres):
    # Update movies genre-wise
    for (genre_id,) in genres:
        # Fetch new movies
        print("Fetching movies of genre id: ", genre_id)
        query = "https://api.themoviedb.org/3/discover/movie?api_key=" + str(api_key) + "&with_genres=" + str(genre_id)
        response =  requests.get(query)
        new_movies_array = []
        if response.status_code == 200:    # API Hit Successful
            movies_json = response.json()
            for d in movies_json["results"]:
                movie_id = d["id"]
                movie_name = d["original_title"]
                new_movies_array.append((movie_id, movie_name))
        else:                              # API Hit Unsuccessful 
            print("Invalid request of movies using genres to API")
            sys.exit(1)

        # Insert into database
        for (movie_id, movie_name) in new_movies_array:
            try:
                # Insert into movies table
                command = 'INSERT INTO movies VALUES (' + str(movie_id) + ',"' + str(movie_name) + '");'
                cursor.execute(command)
                print("Found new movie: ", movie_name)
            except:
                print("Movie already exists in database: ", movie_name)

            try:
                # Insert into genre-movie relation table
                command = "INSERT INTO genre_movie_relation VALUES (" + str(genre_id) + "," + str(movie_id) + ");"
                cursor.execute(command)
            except:
                pass

    # Commit changes to database
    mydb.commit()
        

def fetch_data_and_update_database():
    genres = update_genres()
    update_movies(genres)

# Driver main function
if __name__ == "__main__":
    # Prepare Database
    create_and_use_database()
    create_schema()

    # Fetch data from API and update database
    fetch_data_and_update_database()
