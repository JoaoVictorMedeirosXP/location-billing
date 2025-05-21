from google.cloud import firestore
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE


class FirestoreRepository:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE
        )
        self.client = firestore.Client(credentials=credentials)

    def get_all_contracts(self):
        contracts_data = []
        docs = self.client.collection("rentalContracts").stream()
        for doc in docs:
            data = doc.to_dict()
            contracts_data.append(data)
        return contracts_data
