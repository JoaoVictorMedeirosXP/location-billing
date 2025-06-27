from factories.use_case_factory import make_summary_by_message_use_case
from flask import jsonify, request


def process_summary_by_message_handler():

    body = request.get_json()
    print("BODY:", body)
    message = body.get("message", "")

    use_case = make_summary_by_message_use_case()
    res = use_case.execute(message=message)

    return jsonify(res), 200
