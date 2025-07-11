import pytest
from src.adapters.sheets.sheets_contract_summary_repository import (
    SheetsContractSummaryRepository,
)


@pytest.mark.integration
def test_update_summary_real_planilha():
    # Ajuste para seu nome de aba de teste
    worksheet_name = "TestesRepo"

    repo = SheetsContractSummaryRepository(work_sheet=worksheet_name)

    test_month = "Janeiro"
    test_cnpj = "00.000.000/0000-00"
    # Dados fictícios
    update_data = {
        "month": test_month,
        "cnpj": test_cnpj,
        "values": {
            "Razão Social": "RESTAURANTE TESTE LTDA",
            "Geração Prevista": "10000",
            "Valor Contrato": "9999,99",
            "kWh Injetado": "1000",
            "kWh compensado": "0",
            "porcentagem compensada": "90%",
            "valor aluguel": "1000",
            "porcentagem injetada": "110%",
            "Contas Emitidas": "ok",
        },
    }

    repo.update_summary_row_by_month_and_cnpj(update_data)

    all_values = repo.sheet.get_all_values()

    target_title = f"Cobrança {test_month}"
    title_row_index = None

    for i, row in enumerate(all_values):
        if row and row[0].strip() == target_title:
            title_row_index = i
            break

    assert title_row_index is not None, "Seção não foi criada corretamente"

    header_row = all_values[title_row_index + 1]
    header_map = {col.strip(): idx for idx, col in enumerate(header_row) if col.strip()}

    data_found = False
    for row in all_values[title_row_index + 2 :]:
        if all(cell.strip() == "" for cell in row):
            break
        if (
            len(row) >= header_map["CNPJ"] + 1
            and row[header_map["CNPJ"]].strip() == test_cnpj
        ):
            data_found = True
            for key, value in update_data["values"].items():
                assert row[header_map[key]].strip() == value
            break

    assert data_found, "Linha com CNPJ atualizado não foi encontrada"
