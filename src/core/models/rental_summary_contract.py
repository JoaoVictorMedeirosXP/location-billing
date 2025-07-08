from src.core.models.bill import Bill
from src.core.models.rental_contract import RentalContract
from src.utils.reference_month import ReferenceMonth


class RentalSummaryContract:

    def __init__(
        self,
        rental_contract: RentalContract,
        rental_units_bills: list[Bill],
        units_bills: list[Bill],
        month_reference: ReferenceMonth,
    ):
        self.rental_contract = rental_contract
        self.rental_units_bills = rental_units_bills
        self.units_bills = units_bills
        self.month_reference = month_reference

    @property
    def predicted_generation(self) -> float:
        if self.rental_contract.lot_size != 0:
            return float(self.rental_contract.lot_size)
        return sum(unit["capacity"] for unit in self.rental_contract.rental_units)

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
        if isinstance(self.rental_contract.rent_value, (int, float)):
            return float(self.rental_contract.rent_value)
        value = str(self.rental_contract.rent_value).replace(",", ".")
        return float(value)

    @property
    def proportional_rent(self) -> float:
        return self.full_rent * (self.percent_compensated / 100)

    @property
    def rent(self) -> float:
        if self.compensated_kwh >= self.predicted_generation:
            return self.full_rent
        return self.proportional_rent

    @property
    def percent_injected(self):
        return self.injected_kwh / self.predicted_generation

    @property
    def emitted_bills(self) -> str:
        return f"{len(self.units_bills + self.rental_units_bills)} / {len(self.rental_contract.units) + len(self.rental_contract.rental_units)}"

    def to_dict(self):
        return {
            "month_reference": self.month_reference.as_string,
            "predicted_generation": self.predicted_generation,
            "injected_kwh": self.injected_kwh,
            "compensated_kwh": self.compensated_kwh,
            "percent_compensated": self.percent_compensated,
            "percent_injected": self.percent_injected,
            "full_rent": self.full_rent,
            "proportional_rent": self.proportional_rent,
            "rent": self.rent,
            "rental_contract": (
                self.rental_contract.to_dict()
                if hasattr(self.rental_contract, "to_dict")
                else str(self.rental_contract)
            ),
            "rental_units_bills": [
                bill.to_dict() if hasattr(bill, "to_dict") else str(bill)
                for bill in self.rental_units_bills
            ],
            "units_bills": [
                bill.to_dict() if hasattr(bill, "to_dict") else str(bill)
                for bill in self.units_bills
            ],
        }
