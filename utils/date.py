from datetime import datetime, date

def reference_month(data):
    if isinstance(data, str):
        data = datetime.strptime(data, "%Y-%m-%d")
    elif isinstance(data, date):
        pass
    else:
        raise ValueError("The parameter must be a string 'YYYY-MM-DD' or a object datetime/date.")
    
    return data.strftime("%m/%Y")
