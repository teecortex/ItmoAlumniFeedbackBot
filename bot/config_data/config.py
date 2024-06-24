import os
from dataclasses import dataclass
import dotenv


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str

@dataclass
class TgBot:
    bot_token: str
    admin_ids: list[int]

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig

def load_config(path: str | None = None) -> Config:

    dotenv.load_dotenv(path)
    return Config(
        tg_bot=TgBot(
            bot_token=os.getenv('BOT_TOKEN'),
            admin_ids=[int(i) for i in os.getenv('ADMIN_IDS').split(',')]
        ),
        db=DatabaseConfig(
            database=os.getenv('DATABASE'),
            db_host=os.getenv('DB_HOST'),
            db_user=os.getenv('DB_USER'),
            db_password=os.getenv('DB_PASSWORD')
        )
    )


