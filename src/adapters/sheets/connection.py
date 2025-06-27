import gspread
from config.settings import (
    SERVICE_ACCOUNT_FILE,
)
from google.oauth2 import service_account


class SheetsClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            cls._client = gspread.authorize(credentials)
            print("Starting Sheets Client")
        return cls._client

    @classmethod
    def reset(cls):
        cls._client = None
