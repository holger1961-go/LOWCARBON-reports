from __future__ import annotations

import requests

from ..config_black import API_KEY
from ..utils.logging_setup import logger


API_BASE = "https://api.sitemark.com"

class SitemarkAPI:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"{self.api_key}",
            "Accept": "application/json"
        }
        if not self.api_key:
            logger.warning(
                "Kein SITEMARK API-Key gesetzt."
            )

    def get(self, endpoint: str, params=None):
        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
