from src.core.models.rental_contract import RentalContract
from src.core.repositories.contracts_repository import ContractRepository
from src.core.repositories.units_repository import UnitsRepository
from src.utils.social_document import SocialNumber


class getContractByContractAccountService:

    def __init__(self, units_repo: UnitsRepository, contracts_repo: ContractRepository):

        self.units_repo = units_repo
        self.contracts_repo = contracts_repo

    def exectue(self, account_contract: str) -> RentalContract:

        unit = self.units_repo.get_unit_by_account_contract(account_contract)

        contract_dict = self.contracts_repo.get_contract_by_id(unit["ID DO CONTRATO"])
        all_contract_units = self.units_repo.get_units_by_contract_id(
            contract_dict["ID"]
        )

        return self.make_rental_contract(
            all_units=all_contract_units, contract=contract_dict
        )

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
