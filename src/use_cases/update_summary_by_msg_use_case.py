from src.services.calculate_summary_by_contranct_reference_month_service import (
    calculateSummaryByContranctReferenceMonthService,
)
from src.services.check_unit_is_gd_service import CheckUnitIsGdService
from src.services.get_contract_by_contract_account_service import (
    getContractByContractAccountService,
)
from src.services.update_summary_service import updateSummaryService
from src.utils.reference_month import ReferenceMonth


class UpdateSummaryByMessageUseCase:

    def __init__(
        self,
        check_unit_is_gd_service: CheckUnitIsGdService,
        get_contract_by_contract_account_service: getContractByContractAccountService,
        calculate_summary_by_contranct_reference_month_service: calculateSummaryByContranctReferenceMonthService,
        update_summary_service: updateSummaryService,
    ):

        self.check_unit_is_gd_service = check_unit_is_gd_service
        self.get_contract_by_contract_account_service = (
            get_contract_by_contract_account_service
        )
        self.calculate_summary_by_contranct_reference_month_service = (
            calculate_summary_by_contranct_reference_month_service
        )
        self.update_summary_service = update_summary_service

    def execute(self, message):

        check = self.check_unit_is_gd_service.execute(message["conta_contrato"])

        if not check:
            return {"status": "pass"}

        contract = self.get_contract_by_contract_account_service.exectue(
            message["conta_contrato"]
        )

        reference_month = ReferenceMonth(message["mes_referencia"])

        calculated_summary = (
            self.calculate_summary_by_contranct_reference_month_service.execute(
                contract, reference_month
            )
        )

        self.update_summary_service.execute(summary=calculated_summary)

        return {"status": "success"}
