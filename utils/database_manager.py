from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv, dotenv_values
from utils.config import settings

load_dotenv()
config = dotenv_values(".env")

class DatabaseManager:
    def __init__(self, db_engine: str) -> None:
        self.conn = create_engine(db_engine).connect()

# db_user = "fiknaufalh"
# db_password = "Naoefal#0953"
# db_host = "bevbuddy-beta-server.mysql.database.azure.com"
# db_port = 3306
# db_name = "bevbuddy"
# db_sslmode = "required"

# db_user = config['DB_USER']
# db_password = config['DB_PASSWORD']
# db_host = config['DB_HOST']
# db_port = config['DB_PORT']
# db_name = config['DB_NAME']
# db_sslmode = config['DB_SSLMODE']

db_user = settings.db_username
db_password = settings.db_password
db_host = settings.db_hostname
db_port = settings.db_port
db_name = settings.db_name
db_sslmode = settings.db_sslmode

db_engine = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
dbInstance = DatabaseManager(db_engine)

Session = sessionmaker(autoflush=False, bind=dbInstance.conn)
session = Session()