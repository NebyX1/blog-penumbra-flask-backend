from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
database = os.environ['MYSQL_DATABASE']

# DATABASE_CONNECTION_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# This connection string is just for testing inside local dev setup
DATABASE_CONNECTION_URI = f'mysql+pymysql://{user}@{host}/{database}'
