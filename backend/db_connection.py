import psycopg2
from config import DB_CONFIG 

# postgreSQL connection
connection = psycopg2.connect(**DB_CONFIG)
