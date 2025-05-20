from repositories.bigquery_repository import BigQueryRepository
from repositories.sheets_repository import GoogleSheetsRepository

def main():
    
    
    sheets = GoogleSheetsRepository()
    sheets.append_dataframe(raw_df)
  
    return

if __name__ == "__main__":
    main()