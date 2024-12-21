from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    """

    db_url: str
    password: str
    user: str
    @staticmethod
    def from_env(path: str):
        """
        Creates the DbConfig object from environment variables.
        """

        env = Env()
        env.read_env(path)

        password = env.str("DB_PASS")
        user = env.str("DB_USER")
        db_url = env.str("DB_URL")
        return DbConfig(
            password=password, user=user, db_url=db_url
        )
