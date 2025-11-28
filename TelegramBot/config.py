from dataclasses import dataclass
from typing import Optional

from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass()
class Mistral:
    key: str

@dataclass
class Config:
    tg_bot: TgBot
    mistral: Mistral


def get_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env.str("bot_token")), mistral=Mistral(key=env.str("mistral_key")))


