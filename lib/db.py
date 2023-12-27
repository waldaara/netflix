from dotenv import load_dotenv
import os
import MySQLdb


class MySQL:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            # Load environment variables from the .env file
            load_dotenv()

            # Connect to the database
            cls._instance.connection = MySQLdb.connect(
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USERNAME"),
                passwd=os.getenv("DATABASE_PASSWORD"),
                db=os.getenv("DATABASE"),
                autocommit=True,
                ssl_mode="VERIFY_IDENTITY",
            )
        return cls._instance

    def get_connection(self):
        return self.connection
