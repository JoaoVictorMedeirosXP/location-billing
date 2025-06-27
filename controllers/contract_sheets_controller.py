from factories.use_case_factory import make_legacy_process_contracts_use_case
from flask import jsonify, request


def process_contract_from_sheets_handler():

    body = request.get_json()
    print("BODY:", body)
    target_date = body.get("target_date", "2025-05-01")

    use_case = make_legacy_process_contracts_use_case()
    res = use_case.execute(target_date=target_date)

    return jsonify(res), 200
