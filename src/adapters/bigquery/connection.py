import os
from google.cloud import bigquery
from google.oauth2 import service_account
import google.auth
from config.settings import SERVICE_ACCOUNT_FILE

class BigQueryClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            if SERVICE_ACCOUNT_FILE and os.path.exists(SERVICE_ACCOUNT_FILE):
                credentials = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE
                )
                cls._client = bigquery.Client(credentials=credentials)
                print("Starting BigQuery Client with explicit credentials")
            else:
                credentials, _ = google.auth.default()
                cls._client = bigquery.Client(credentials=credentials)
                print("Starting BigQuery Client with default credentials")
        return cls._client

    @classmethod
    def reset(cls):
        cls._client = None
