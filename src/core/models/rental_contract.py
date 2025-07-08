from datetime import date

from src.utils.cnpj import CNPJ


class RentalContract:

    def __init__(
        self,
        calculation_method: str,
        contractDate: date,
        name: str,
        rent_value: float,
        rental_units: list[dict],
        units: list[dict],
        cnpj: CNPJ,
        lot_size: float = 0
    ):

        self.calculation_method = calculation_method
        self.contractDate = contractDate
        self.name = name
        self.rent_value = rent_value
        self.rental_units = rental_units
        self.units = units
        self.cnpj = cnpj
        self.lot_size = lot_size

    @property
    def all_contract_codes(self) -> list[str]:
        key_account_contract = "contractAccount" if "contractAccount" in self.units[0].keys() else "CONTA CONTRATO"
        unit_codes = [i[key_account_contract] for i in self.units]
        rental_units_codes = [i[key_account_contract] for i in self.rental_units]

        return unit_codes + rental_units_codes
    
