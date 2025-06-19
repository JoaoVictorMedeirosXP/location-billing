from flask import request, jsonify
from factories.use_case_factory import make_legacy_process_contracts_use_case


def process_contract_from_sheets_handler():
   
    body = request.get_json()
    print("BODY:",body)
    target_date = body.get("target_date", "2025-05-01")

    use_case = make_legacy_process_contracts_use_case()
    count = use_case.execute(target_date=target_date)

    return jsonify({"status": "success", "written_rows": count}), 200


    return jsonify({"status": "error", "message": str(e)}), 500
