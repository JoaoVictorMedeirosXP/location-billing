from datetime import date, datetime


class ReferenceMonth:
    SUPPORTED_FORMATS = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%Y",
    ]

    MONTHS_PT = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    def __init__(self, value):
        self._original_value = value
        self._date = self._parse_to_date(value)

    @classmethod
    def current(cls):
        return cls(date.today())

    def _parse_to_date(self, value):
        if isinstance(value, datetime | date):
            return value
        elif isinstance(value, str):
            for fmt in self.SUPPORTED_FORMATS:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            raise ValueError(
                "String must be in one of the following formats: "
                "'YYYY-MM-DD', 'DD/MM/YYYY', or 'MM/YYYY'."
            )
        else:
            raise ValueError(
                "Value must be a string in accepted formats, or a date/datetime object."
            )

    @property
    def as_string(self) -> str:
        return self._date.strftime("%m/%Y")
    
    @property
    def as_firestore_string(self) -> str:
        return f"{self._date.year}-{self._date.month:02d}-01T03:00:00+00:00"

    @property
    def as_date(self) -> date:
        return self._date if isinstance(self._date, date) else self._date.date()

    @property
    def as_full_month_pt(self) -> str:
        month_index = self._date.month - 1
        year = self._date.year
        month_name_pt = self.MONTHS_PT[month_index]
        return f"{month_name_pt} de {year}"
