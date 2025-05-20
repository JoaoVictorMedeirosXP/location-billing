from google.cloud import bigquery
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE

class BigQueryRepository:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE
        )
        self.client = bigquery.Client(credentials=credentials)

    def run_query(self, query: str):
        return self.client.query(query).to_dataframe()
