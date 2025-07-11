from flask import jsonify, request
from src.factories.use_case_factory import make_update_summary_by_msg_use_case


def process_update_summary_by_message_handler():

    body = request.get_json()
    print("BODY:", body)
    message = body.get("message", "")

    use_case = make_update_summary_by_msg_use_case()
    res = use_case.execute(message=message)

    return jsonify(res), 200
