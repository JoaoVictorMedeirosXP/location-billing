from src.adapters.firestore.connection import FirestoreClientSingleton
from src.core.models.bill import Bill
from src.core.repositories.bills_repository import BillRepository
from src.utils.reference_month import ReferenceMonth


class FirestoreBillsRepository(BillRepository):

    def __init__(self):
        self.client = FirestoreClientSingleton.get_client()

    def get_bills_by_contracts_and_month(self, all_account_contracts, reference_month: ReferenceMonth):
        bills = []
        chunk_size = 10

        for i in range(0, len(all_account_contracts), chunk_size):
            chunk = all_account_contracts[i : i + chunk_size]
            query = (
                self.client.collection("faturas_processadas")
                .where("dados.unidade_consumidora.contrato", "in", chunk)
                .where("dados.fatura.mes_referencia", "==", reference_month.as_firestore_string)
            )
            
            print(reference_month.as_firestore_string)

            docs = query.stream()
            for doc in docs:
                print(doc)
                bills.append(self.make_bill(doc.to_dict()))

        return bills

    def make_bill(self, document) -> Bill:
        dados = document["dados"]

        return Bill(
            concessionaria=dados["distribuidora"],
            mes_referencia=dados["fatura"]["mes_referencia"],            
        )
