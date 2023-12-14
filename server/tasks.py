import os
from datetime import timedelta
import pandas as pd
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def fill_sales_data(identifier):
    df = pd.read_excel(os.path.join('sales_data', f'{identifier}.xlsx')).fillna('')
    df.columns = df.columns.str.lower()

    df['date'] = pd.to_datetime(df['date']).dt.date

    start_date = df['date'].min()
    end_date = df['date'].max()

    sales_list = []
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date not in df['date'].values:
            sales_data = None
        else:
            sales_data = df[df['date'] == start_date]['sales'].sum()
        sales_list.append((start_date, sales_data))
        start_date += delta

    new_df = pd.DataFrame(sales_list, columns=['Date', 'Sales'])
    new_df['Sales'] = pd.to_numeric(new_df['Sales'], errors='coerce')
    new_df['Sales'].interpolate(method='linear', inplace=True)

    return {str(identifier) :new_df.to_dict('records')}
