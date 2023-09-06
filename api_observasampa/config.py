

from core.utils.utils import build_conn_str
from dotenv import load_dotenv
import os

load_dotenv(os.path.join('..', '.env'))

db_data = {
'host': os.environ['HOST'],
'port': os.environ['PORT'],
'database': os.environ['DB'],
'user': os.environ['USER'],
'password': os.environ['PASSW']
}


SQLALCHEMY_DATABASE_URL = build_conn_str(**db_data)
REQUEST_TIMEOUT_ERROR=os.environ['REQUEST_TIMEOUT_ERROR']

        