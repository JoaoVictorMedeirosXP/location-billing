from flask import Blueprint
from controllers.contract_sheets_controller import process_contract_from_sheets_handler

contract_sheet_blueprint = Blueprint("contract-sheet", __name__)

# POST /contract-sheet/
contract_sheet_blueprint.route("/", methods=["POST"])(process_contract_from_sheets_handler)