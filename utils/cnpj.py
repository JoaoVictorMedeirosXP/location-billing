import re


class CNPJ:
    def __init__(self, cnpj):
        if isinstance(cnpj, int):
            raw = str(cnpj)
        elif isinstance(cnpj, str):
            raw = self._clean(cnpj)
        else:
            raise TypeError("CNPJ must be a string or an integer.")

        if len(raw) < 14:
            raw = raw.zfill(14)

        self.raw = raw

        if not self._is_valid():
            raise ValueError(f"Invalid CNPJ: {cnpj}")

    def _clean(self, cnpj: str) -> str:
        """Remove all non-digit characters."""
        return re.sub(r"\D", "", cnpj)

    def _is_valid(self) -> bool:
        """Validate the CNPJ using verification digits."""
        cnpj = self.raw
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        def calculate_check_digit(cnpj, weights):
            total = sum(int(digit) * weight for digit, weight in zip(cnpj, weights))
            remainder = total % 11
            return "0" if remainder < 2 else str(11 - remainder)

        dv1 = calculate_check_digit(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        dv2 = calculate_check_digit(
            cnpj[:12] + dv1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        )
        return cnpj[-2:] == dv1 + dv2

    @property
    def formatted(self) -> str:
        """Return the CNPJ in the format: 00.000.000/0000-00"""
        c = self.raw
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"

    @property
    def numbered(self):
        return self.raw

    def __eq__(self, other):
        if isinstance(other, CNPJ):
            return self.raw == other.raw
        elif isinstance(other, str):
            other_clean = self._clean(other).zfill(14)
            return self.raw == other_clean
        elif isinstance(other, int):
            other_str = str(other).zfill(14)
            return self.raw == other_str
        return NotImplemented

    def __hash__(self):
        return hash(self.raw)

    def __str__(self):
        return self.formatted()

    def __repr__(self):
        return self.formatted()
