from flask import Flask
from src.routes.contract_sheets_routes import contract_sheet_blueprint
from src.routes.summary_by_message_routes import summary_by_message_blueprint
from src.routes.update_summary_by_message_routes import (
    update_summary_by_message_blueprint,
)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(contract_sheet_blueprint, url_prefix="/contract-sheet")
    app.register_blueprint(
        summary_by_message_blueprint, url_prefix="/summary-by-message"
    )
    app.register_blueprint(
        update_summary_by_message_blueprint, url_prefix="/update-by-message"
    )
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
