from config.settings import SERVICE_ACCOUNT_FILE
from google.cloud import firestore
from google.oauth2 import service_account


class FirestoreClientSingleton:

    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE
            )
            cls._client = firestore.Client(credentials=credentials)
            print("Starting Firestore Client")
        return cls._client

    @classmethod
    def reset(cls):
        cls._client = None
