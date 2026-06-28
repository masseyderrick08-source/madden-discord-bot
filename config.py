from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlencode

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    discord_bot_token: str
    discord_application_id: int | None
    ea_auth_source: str
    ea_client_id: str
    ea_client_secret: str
    ea_redirect_url: str
    ea_machine_key: str
    token_encryption_key: str
    database_path: str

    @property
    def ea_login_url(self) -> str:
        params = {
            "hide_create": "true",
            "release_type": "prod",
            "response_type": "code",
            "redirect_uri": self.ea_redirect_url,
            "client_id": self.ea_client_id,
            "machineProfileKey": self.ea_machine_key,
            "authentication_source": self.ea_auth_source,
        }
        return f"https://accounts.ea.com/connect/auth?{urlencode(params)}"


def load_settings() -> Settings:
    application_id = os.getenv("DISCORD_APPLICATION_ID")
    return Settings(
        discord_bot_token=_required("DISCORD_BOT_TOKEN"),
        discord_application_id=int(application_id) if application_id else None,
        ea_auth_source=os.getenv("EA_AUTH_SOURCE", "317239"),
        ea_client_id=os.getenv("EA_CLIENT_ID", "MCA_26_COMP_APP"),
        ea_client_secret=_required("EA_CLIENT_SECRET"),
        ea_redirect_url=os.getenv("EA_REDIRECT_URL", "http://127.0.0.1/success"),
        ea_machine_key=os.getenv("EA_MACHINE_KEY", "444d362e8e067fe2"),
        token_encryption_key=_required("TOKEN_ENCRYPTION_KEY"),
        database_path=os.getenv("DATABASE_PATH", "data/madden26_bot.sqlite3"),
    )

