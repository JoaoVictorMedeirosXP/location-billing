from utils.cnpj import CNPJ


class RentalContract:

    def __init__(
        self,
        calculation_method,
        contractDate,
        name,
        rent_value,
        rental_units,
        units,
        cnpj: CNPJ,
    ):
        self.calculation_method = calculation_method
        self.contractDate = contractDate
        self.name = name
        self.rent_value = rent_value
        self.rental_units = rental_units
        self.units = units
        self.cnpj = cnpj
        return
