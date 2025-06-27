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
    ):

        self.calculation_method = calculation_method
        self.contractDate = contractDate
        self.name = name
        self.rent_value = rent_value
        self.rental_units = rental_units
        self.units = units
        self.cnpj = cnpj

    @property
    def all_contract_codes(self) -> list[str]:
        unit_codes = [i["contractAccount"] for i in self.units]
        rental_units_codes = [i["contractAccount"] for i in self.rental_units]

        return unit_codes + rental_units_codes
