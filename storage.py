from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet


@dataclass(frozen=True)
class StoredAccount:
    discord_user_id: int
    console: str
    token: dict[str, Any]


class TokenStore:
    def __init__(self, database_path: str, encryption_key: str) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.fernet = Fernet(encryption_key.encode())
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ea_accounts (
                    discord_user_id INTEGER PRIMARY KEY,
                    console TEXT NOT NULL,
                    encrypted_token TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save_account(self, discord_user_id: int, console: str, token: dict[str, Any]) -> None:
        encrypted_token = self.fernet.encrypt(json.dumps(token).encode()).decode()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO ea_accounts (discord_user_id, console, encrypted_token, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(discord_user_id)
                DO UPDATE SET
                    console = excluded.console,
                    encrypted_token = excluded.encrypted_token,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (discord_user_id, console, encrypted_token),
            )

    def get_account(self, discord_user_id: int) -> StoredAccount | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT console, encrypted_token FROM ea_accounts WHERE discord_user_id = ?",
                (discord_user_id,),
            ).fetchone()
        if not row:
            return None
        console, encrypted_token = row
        token = json.loads(self.fernet.decrypt(encrypted_token.encode()).decode())
        return StoredAccount(discord_user_id=discord_user_id, console=console, token=token)

    def delete_account(self, discord_user_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM ea_accounts WHERE discord_user_id = ?",
                (discord_user_id,),
            )
            return cursor.rowcount > 0

