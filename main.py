from services.bigquery_service import BigQueryService
from services.sheets_service import GoogleSheetsService

QUERY = """
    SELECT *
    FROM `xperesidencial.big_data.bills_big_data` 
    WHERE conta_contrato = '7051194750'
"""

def main():
    bq = BigQueryService()
    raw_df = bq.run_query(QUERY)
    
    sheets = GoogleSheetsService()
    sheets.append_dataframe(raw_df)
  
    return

if __name__ == "__main__":
    main()