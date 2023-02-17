# PubliQ-Demo

This demo project uses Python to create a MySQL movie database and populate it using the data fetched from TMDB (The Movie DataBase) API. This is created as part of my job application for the role of Data Engineer at PubliQ. 

## Running Instructions

1. This project requires Python3 installed on the concerned system
2. Install the dependencies provided in the file [requirements.txt](./config/requirements.txt)
```
pip install -r requirements.txt
```
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
(For testing on localhost database, please install and setup MySQL first on the concerned system)