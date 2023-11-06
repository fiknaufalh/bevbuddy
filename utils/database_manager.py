from sqlalchemy import create_engine, text
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

class DatabaseManager:
    def __init__(self, db_engine: str) -> None:
        self.conn = create_engine(db_engine).connect()

db_user = config['DB_USER']
db_password = config['DB_PASSWORD']
db_host = config['DB_HOST']
db_port = config['DB_PORT']
db_database = config['DB_DATABASE']
db_sslmode = config['DB_SSLMODE']

db_engine = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}?sslmode={db_sslmode}"
dbInstance = DatabaseManager(db_engine)