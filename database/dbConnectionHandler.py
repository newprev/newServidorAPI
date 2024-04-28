from pathlib import Path
from os import getenv

from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker


class DBConnHandler:
    def __init__(self):
        self.__connection_url = self.__geraUrlConnection()
        self.__engine = self.__create_db_engine()
        self.session = None

    def __geraUrlConnection(self) -> URL:
        # Carregando variáveis de ambiente
        pathEnvVars = Path('.') / '.env'
        if not pathEnvVars.is_file():
            print(f'{pathEnvVars.absolute()=}')
            raise Exception('Não foi possível encontrar o arquivo com as variáveis de ambiente.')
        else:
            load_dotenv(pathEnvVars.absolute())

        return URL.create(
            "mysql+pymysql",
            username=getenv('DB_USER'),
            password=getenv('DB_PASS'),
            host=getenv('DB_HOST', 'localhost'),
            database=getenv('DB_NAME')
        )

    def __create_db_engine(self):
        return create_engine(self.__connection_url)

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        sessionMake = sessionmaker(bind=self.__engine)
        self.session = sessionMake()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()