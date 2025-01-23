import requests
import logging
from django.conf import settings


class CRYPTOAPI:

    base_url = getattr(settings, "CRYPTO_GECO_BASE_URL")

    def _get_data(cls, endpoint, params=None):
        """
        Handles the HTTP Requests to the Crypto API
        args:
            endpoints: The API endpoint to Call
            params: Query Parameters for the API call
        """
        url = f"{cls.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(
                "HTTP error occurred: %s %s", e.response.status_code, e.response.reason
            )
            raise RuntimeError(
                "API request failed with status: %s", e.response.status_code
            )
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error occurred: {e}")
            raise RuntimeError("Failed to fetch data from Crypto API.")

    @classmethod
    def get_coins(cls):
        """
        API to Fetch all the Coins List.
        """
        return cls._get_data(cls, endpoint="coins/list")

    @classmethod
    def get_coinCategory(cls):
        """
        API to Fetch all the Coins Categories
        """
        return cls._get_data(cls, endpoint="coins/categories/list")

    @classmethod
    def fetch_market_data(
        cls, ids=None, category=None, vs_currency="cad", per_page=10, page=1
    ):
        """
        Fetches market data for coins based on IDs or category.
        - ids: Comma-separated coin IDs.
        - category: Specific category of coins.
        - vs_currency: Currency for price conversion (default is CAD).
        - per_page: Number of results per page.
        - page: Page number.
        """
        params = {
            "vs_currency": vs_currency,
            "ids": ids,
            "category": category,
            "per_page": per_page,
            "page": page,
        }
        return cls._get_data(cls, endpoint="coins/markets", params=params)
