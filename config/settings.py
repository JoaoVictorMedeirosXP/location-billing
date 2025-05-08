from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SERVICE_ACCOUNT_FILE = BASE_DIR / "credentials/service_account.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1d1WIGeyyKBkRWNz4j6kHkX5FPXrecQdEHO_ZxBq8ADw/"
SHEET_NAME = "aba_test"
NUM_ROWS_TO_JUMP = 2
