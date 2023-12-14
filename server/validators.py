import pandas as pd
from datetime import datetime


def validate_file(file):
    try:
        df = pd.read_excel(file).fillna(0)
    except:
        return ['could not open file']
    
    errors = []
    df.columns = df.columns.str.lower()
    dates = True
    sales = True
    if 'date' not in df.columns:
        dates = False
        errors.append('\'Date\' column is absent in excel')
    else:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    if 'sales' not in df.columns:
        sales = False
        errors.append('\'Sales\' column is asbent in excel')
    else:
        df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    if df.empty:
        errors.append('excel is empty')
        return errors
    
    for index, row in df.iterrows():
        if dates:
            date = str(row['date']).split(' ')[0]
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except:
                errors.append(f'row {index+1}: date does not match format YYYY-MM-DD')
        if sales:
            sales_amount = row['sales']
            if sales_amount and not isinstance(sales_amount, float):
                errors.append(f'row {index+1}: float expected')
    return errors
