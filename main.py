from flask import Flask
from routes.contract_sheets_routes import contract_sheet_blueprint


def create_app():
    app = Flask(__name__)

    app.register_blueprint(contract_sheet_blueprint, url_prefix="/contract-sheet")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
