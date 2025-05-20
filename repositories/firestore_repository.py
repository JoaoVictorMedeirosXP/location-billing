from google.cloud import firestore
from datetime import datetime

class FirestoreRepository:
    def __init__(self):
        self.client = firestore.Client()
  
    def get_all_contracts(self):
        contracts_data = []
        docs = db.collection('rentalContracts').stream()
        for doc in docs:
            data = doc.to_dict()
            contracts_data.append(data)
        return contracts_data
