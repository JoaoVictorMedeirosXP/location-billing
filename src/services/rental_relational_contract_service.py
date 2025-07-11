from src.core.models.rental_contract import RentalContract
from src.core.models.rental_summary_contract import RentalSummaryContract
from src.core.repositories.bills_repository import BillRepository
from src.core.repositories.contracts_repository import ContractRepository
from src.core.repositories.contracts_summary_repository import ContractSummaryRepository
from src.core.repositories.units_repository import UnitsRepository
from src.utils.reference_month import ReferenceMonth
from src.utils.social_document import SocialNumber


class RentalRelationalContractService:

    def __init__(
        self,
        units_repo: UnitsRepository,
        contract_repo: ContractRepository,
        bills_repo: BillRepository,
    ):
        self.units_repo = units_repo
        self.contract_repo = contract_repo
        self.bills_repo = bills_repo

    def execute(self) -> list[ContractSummaryRepository]:

        all_contracts = self.contract_repo.get_all_contracts()

        rental_contracts = []
        for contract in all_contracts:
            all_units = self.units_repo.get_units_by_contract_id(contract["ID"])
            rental_contracts.append(self.make_rental_contract(contract, all_units))

        summaries = []
        for rental_contract in rental_contracts:
            summaries.append(self.make_rental_contract_summary(rental_contract))
        return summaries

    def make_rental_contract(self, contract, all_units) -> RentalContract:

        units = [i for i in all_units if i["UNIDADE DE ENVIO DE BOLETO"] == "SIM"]
        rental_units = [
            i for i in all_units if i["UNIDADE DE ENVIO DE BOLETO"] == "NÃO"
        ]

        return RentalContract(
            calculation_method=contract["MÉTODO DE CÁLCULO"],
            cnpj=SocialNumber(contract["CNPJ"]),
            contractDate=contract["INÍCIO CONTRATO"],
            name=contract["APELIDO"],
            rent_value=contract["VALOR CONTRATO"],
            rental_units=rental_units,
            units=units,
            lot_size=contract["TAMANHO LOTE (KWH)"],
        )

    def make_rental_contract_summary(
        self, rental_contract: RentalContract
    ) -> RentalSummaryContract:

        month_reference = ReferenceMonth(value="06/2025")
        # month_reference = ReferenceMonth.current()

        bills = self.bills_repo.get_bills_by_contracts_and_month(
            all_account_contracts=rental_contract.all_contract_codes,
            reference_month=month_reference,
        )

        unit_accounts = [unit["CONTA CONTRATO"] for unit in rental_contract.units]
        rental_unit_accounts = [
            unit["CONTA CONTRATO"] for unit in rental_contract.rental_units
        ]


        return RentalSummaryContract(
            rental_contract=rental_contract,
            month_reference=month_reference,
            units_bills=[
                bill for bill in bills if bill.conta_contrato in unit_accounts
            ],
            rental_units_bills=[
                bill for bill in bills if bill.conta_contrato in rental_unit_accounts
            ],
        )
