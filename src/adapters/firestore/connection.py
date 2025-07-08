import os
from google.cloud import firestore
from google.oauth2 import service_account
import google.auth
from config.settings import SERVICE_ACCOUNT_FILE

class FirestoreClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            if SERVICE_ACCOUNT_FILE and os.path.exists(SERVICE_ACCOUNT_FILE):
                credentials = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE
                )
                cls._client = firestore.Client(credentials=credentials)
                print("Starting Firestore Client with explicit credentials")
            else:
                credentials, _ = google.auth.default()
                cls._client = firestore.Client(credentials=credentials)
                print("Starting Firestore Client with default credentials")
        return cls._client

    @classmethod
    def reset(cls):
        cls._client = None
