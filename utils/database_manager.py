from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from utils.config import settings

class DatabaseManager:
    def __init__(self, db_engine: str) -> None:
        self.conn = create_engine(db_engine).connect()

db_username = settings.db_username
db_password = settings.db_password
db_hostname = settings.db_hostname
db_port = settings.db_port
db_name = settings.db_name
db_sslmode = settings.db_sslmode

db_engine = f"mysql+pymysql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"
dbInstance = DatabaseManager(db_engine)

Session = sessionmaker(autoflush=False, bind=dbInstance.conn)
session = Session()