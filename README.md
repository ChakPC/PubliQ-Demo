# PubliQ-Demo

This demo project uses Python to create a MySQL movie database and populate it using the data fetched from TMDB (The Movie DataBase) API. This is created as part of my job application for the role of Data Engineer at PubliQ. 

## Database Schema

There are two tables ```genres``` and ```movies``` and there is a relation table between them called ```genre_movie_relation```. The schema of the tables can be found in SQL files provided in [SQL](./SQL/) folder. There is a many-to-many mapping between data points of both these tables.

## API Details

The [TMDB](https://www.themoviedb.org/) API is useful for getting various details about movies. I have used two services of this API.

1. Fetching list of all genres (Link: [Docs](https://developers.themoviedb.org/3/genres))
2. Fetching movies of a specific genre (Link: [Docs](https://developers.themoviedb.org/3/discover/movie-discover))

## System Requirements

1. This project requires Python3 installed on the concerned system
2. If you do not want to activate virtual environment then you can separately install the dependencies provided in the file [requirements.txt](./config/requirements.txt)
```
pip install -r requirements.txt
```
3. This project is developed and tested on the Ubuntu 20.04 operating system. Therefore, it can run in any Linux or MacOS system. However, compatibility for Windows hasn't been checked as this is a demo project.  

## Running Instructions

1. Clone this repository into the concerned system and navigate to the project directory.
2. You can use the virtual environment provided along with this project in Linux or MacOS systems. On the terminal, use the command
```
source env/bin/activate
```
to activate virtual environment which has all the required dependencies.
3. Request for your own API keys on [TMDB](https://www.themoviedb.org/) website
4. Setup your MySQL database and get its credentials (host name, database name, username, password, port). This can be a localhost database or any cloud hosted database. 
4. Create a .env file in [config](./config/) folder to store your API key and Database credentials. Please follow this example for variable naming conventions:
```
api_key = "************"
api_key_v4 = "************"
db_host = "**************"
db_name = "PubliQDemoDB"
db_user = "************"
db_password = "*********"
db_port = "************"
```
5. You are all set now to run the project and store movies in your own database. Just open terminal in the project directory and execute the following command
```
python3 main.py
```