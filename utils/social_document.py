import re

from utils.cnpj import CNPJ
from utils.cpf import CPF


class SocialNumber:
    def __init__(self, value, validate=True):
        cleaned = self._clean(str(value))

        if len(cleaned) <= 11:
            self.document = CPF(cleaned.zfill(11), validate=validate)
        elif len(cleaned) <= 14:
            self.document = CNPJ(cleaned.zfill(14), validate=validate)
        else:
            raise ValueError(
                "Invalid social number: it must have up to 11 (CPF) or 14 (CNPJ) characteres."
            )

    def _clean(self, value: str) -> str:
        return re.sub(r"\D", "", value)

    @property
    def formatted(self) -> str:
        return self.document.formatted

    @property
    def numbered(self) -> str:
        return self.document.numbered

    def is_cpf(self) -> bool:
        return isinstance(self.document, CPF)

    def is_cnpj(self) -> bool:
        return isinstance(self.document, CNPJ)

    def is_valid(self) -> bool:
        return self.document.is_valid()

    def __str__(self):
        return str(self.document)

    def __repr__(self):
        return repr(self.document)

    def __eq__(self, other):
        if isinstance(other, SocialNumber):
            return self.numbered == other.numbered
        return self.numbered == str(other)

    def __hash__(self):
        return hash(self.numbered)
