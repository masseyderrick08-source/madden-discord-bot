from __future__ import annotations

from typing import Any

import aiohttp

from src.config import Settings


class EAClientError(RuntimeError):
    pass


class EAClient:
    TOKEN_URL = "https://accounts.ea.com/connect/token"
    TOKEN_INFO_URL = "https://accounts.ea.com/connect/tokeninfo"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def login_url(self) -> str:
        return self.settings.ea_login_url

    async def exchange_code(self, code: str) -> dict[str, Any]:
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.settings.ea_client_id,
            "client_secret": self.settings.ea_client_secret,
            "redirect_uri": self.settings.ea_redirect_url,
        }
        return await self._post_form(self.TOKEN_URL, payload)

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.settings.ea_client_id,
            "client_secret": self.settings.ea_client_secret,
        }
        return await self._post_form(self.TOKEN_URL, payload)

    async def token_info(self, access_token: str) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.TOKEN_INFO_URL,
                params={"access_token": access_token},
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                return await self._json_or_error(response)

    async def _post_form(self, url: str, payload: dict[str, str]) -> dict[str, Any]:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                data=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                return await self._json_or_error(response)

    async def _json_or_error(self, response: aiohttp.ClientResponse) -> dict[str, Any]:
        text = await response.text()
        if response.status >= 400:
            raise EAClientError(f"EA request failed with HTTP {response.status}: {text[:500]}")
        try:
            data = await response.json(content_type=None)
        except Exception as exc:
            raise EAClientError(f"EA returned non-JSON response: {text[:500]}") from exc
        if not isinstance(data, dict):
            raise EAClientError("EA returned an unexpected response shape.")
        return data

