from controllers.summary_by_message_controller import process_summary_by_message_handler
from flask import Blueprint

summary_by_message_blueprint = Blueprint("summary-by-message", __name__)

# POST /summary-by-message/
summary_by_message_blueprint.route("/", methods=["POST"])(
    process_summary_by_message_handler
)
