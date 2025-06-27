from src.utils.document import REMAINDER_CONST, Document

CPF_LENGTH = 11


class CPF(Document):
    @property
    def length(self) -> int:
        return CPF_LENGTH

    def _is_valid(self) -> bool:
        cpf = self.raw
        if len(cpf) != CPF_LENGTH or cpf == cpf[0] * CPF_LENGTH:
            return False

        def calculate_check_digit(partial, weights):
            total = sum(int(d) * w for d, w in zip(partial, weights, strict=False))
            remainder = total % CPF_LENGTH
            return "0" if remainder < REMAINDER_CONST else str(CPF_LENGTH - remainder)

        dv1 = calculate_check_digit(cpf[:9], range(10, 1, -1))
        dv2 = calculate_check_digit(cpf[:9] + dv1, range(CPF_LENGTH, 1, -1))
        return cpf[-2:] == dv1 + dv2

    @property
    def formatted(self) -> str:
        c = self.raw
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
