from utils.cpf import CPF_LENGTH
from utils.document import REMAINDER_CONST, Document

CNPJ_LENGTH = 14


class CNPJ(Document):
    @property
    def length(self) -> int:
        return CNPJ_LENGTH

    def _is_valid(self) -> bool:
        cnpj = self.raw
        if len(cnpj) != CNPJ_LENGTH or cnpj == cnpj[0] * CNPJ_LENGTH:
            return False

        def calculate_check_digit(partial, weights):
            total = sum(int(d) * w for d, w in zip(partial, weights, strict=False))
            remainder = total % CPF_LENGTH
            return "0" if remainder < REMAINDER_CONST else str(CPF_LENGTH - remainder)

        dv1 = calculate_check_digit(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        dv2 = calculate_check_digit(
            cnpj[:12] + dv1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        )
        return cnpj[-2:] == dv1 + dv2

    @property
    def formatted(self) -> str:
        c = self.raw
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"
