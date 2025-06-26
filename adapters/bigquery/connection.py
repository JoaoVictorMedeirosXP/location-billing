from google.cloud import bigquery
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE


class BigQueryClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE
            )
            cls._client = bigquery.Client(credentials=credentials)
            print("Starting Big Query Client")
        return cls._client

    @classmethod
    def reset(cls):
        cls._client = None
