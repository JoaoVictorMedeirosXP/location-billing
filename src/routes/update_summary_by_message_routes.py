from flask import Blueprint
from src.controllers.update_summary_by_msg_controller import (
    process_update_summary_by_message_handler,
)

update_summary_by_message_blueprint = Blueprint("update-by-message", __name__)

# POST /update-by-message/
update_summary_by_message_blueprint.route("/", methods=["POST"])(
    process_update_summary_by_message_handler
)
