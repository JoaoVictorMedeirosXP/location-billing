from utils.document import Document


class CPF(Document):
    @property
    def length(self) -> int:
        return 11

    def _is_valid(self) -> bool:
        cpf = self.raw
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        def calculate_check_digit(partial, weights):
            total = sum(int(d) * w for d, w in zip(partial, weights, strict=False))
            remainder = total % 11
            return "0" if remainder < 2 else str(11 - remainder)

        dv1 = calculate_check_digit(cpf[:9], range(10, 1, -1))
        dv2 = calculate_check_digit(cpf[:9] + dv1, range(11, 1, -1))
        return cpf[-2:] == dv1 + dv2

    @property
    def formatted(self) -> str:
        c = self.raw
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
