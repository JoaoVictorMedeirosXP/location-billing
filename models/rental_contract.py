from utils.cnpj import CNPJ
from models.bill import Bill

from datetime import date
from typing import List


class RentalContract:

    def __init__(
        self,
        calculation_method: str,
        contractDate: date,
        name: str,
        rent_value: float,
        rental_units: List[dict],
        units: List[dict],
        rental_units_bills: List[Bill],
        units_bills: List[Bill],
        cnpj: CNPJ,
        month_reference: str,
    ):
        self.calculation_method = calculation_method
        self.contractDate = contractDate
        self.name = name
        self.rent_value = rent_value
        self.rental_units = rental_units
        self.units = units
        self.rental_units_bills = rental_units_bills
        self.units_bills = units_bills
        self.cnpj = cnpj
        self.month_reference = month_reference

    @property
    def predicted_generation(self) -> float:
        return sum(unit["capacity"] for unit in self.rental_units)

    @property
    def injected_kwh(self) -> float:
        return sum([bill.energia_injetada for bill in self.rental_units_bills])

    @property
    def compensated_kwh(self) -> float:
        return sum([bill.energia_compensada for bill in self.units_bills])

    @property
    def percent_compensated(self) -> float:
        return (self.compensated_kwh / self.predicted_generation) * 100

    @property
    def full_rent(self) -> float:
        return self.rent_value

    @property
    def proportional_rent(self) -> float:
        return self.rent_value * (self.percent_compensated / 100)

    @property
    def rent(self) -> float:
        if self.compensated_kwh >= self.predicted_generation:
            return self.full_rent
        return self.proportional_rent

    @property
    def percent_injected(self):
        return self.injected_kwh / self.predicted_generation
