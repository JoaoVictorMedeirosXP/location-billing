import os

import google.auth
import gspread
from config.settings import SERVICE_ACCOUNT_FILE
from google.oauth2 import service_account


class SheetsClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            if SERVICE_ACCOUNT_FILE and os.path.exists(SERVICE_ACCOUNT_FILE):
                credentials = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=SCOPES
                )
                print("Starting Sheets Client with explicit credentials")
            else:
                credentials, _ = google.auth.default(scopes=SCOPES)
                print("Starting Sheets Client with default credentials")
            cls._client = gspread.authorize(credentials)
        return cls._client

    @classmethod
    def reset(cls):
        cls._client = None
