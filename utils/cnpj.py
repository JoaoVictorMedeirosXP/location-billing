from utils.document import Document


class CNPJ(Document):
    @property
    def length(self) -> int:
        return 14

    def _is_valid(self) -> bool:
        cnpj = self.raw
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        def calculate_check_digit(partial, weights):
            total = sum(int(d) * w for d, w in zip(partial, weights, strict=False))
            remainder = total % 11
            return "0" if remainder < 2 else str(11 - remainder)

        dv1 = calculate_check_digit(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        dv2 = calculate_check_digit(
            cnpj[:12] + dv1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        )
        return cnpj[-2:] == dv1 + dv2

    @property
    def formatted(self) -> str:
        c = self.raw
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"
