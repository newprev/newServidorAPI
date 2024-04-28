from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

# Carregando variáveis de ambiente
pathEnvVars = Path('.') / '.env'
if not pathEnvVars.is_file():
    print(f'{pathEnvVars.absolute()=}')
    raise Exception('Não foi possível encontrar o arquivo com as variáveis de ambiente.')
else:
    load_dotenv(pathEnvVars.absolute())

urlConn = URL.create(
    "mysql+pymysql",
    username=getenv('DB_USER'),
    password=getenv('DB_PASS'),
    host=getenv('DB_HOST', 'localhost'),
    database=getenv('DB_NAME')
)

engine = create_engine(urlConn)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
