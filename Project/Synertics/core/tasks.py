# myapp/tasks.py

from celery import shared_task
from datetime import datetime
from celery.schedules import crontab
from Synertics.celery import app

from io import BytesIO
import requests
import pandas as pd
from .models import Trade

import logging
logging.basicConfig(level=logging.INFO)

@shared_task(name='daily_scrape')
def daily_scrape():
    
    
    current_time = datetime.now().strftime("%Y%m%d")
    logging.info(f"Starting daily scrape at {current_time}")
    
    url=f"https://www.enexgroup.gr/documents/20126/314344/{current_time}_DER_DOL_EN_v01.xlsx"
    logging.info(f"Fetching data from URL: {url}")

    xlsData=fetch_url(url)
    if xlsData.empty:
        logging.error(f"No data found for the date: {current_time}")
        return "No data found for the given date."
    logging.info(f"Data fetched successfully for the date: {current_time}")
    store_data(xlsData)

    return f"Daily task completed at {current_time}"

def fetch_url(url):
     response = requests.get(url)
     logging.info(f"Response status code: {response.status_code}")
     
     if response.status_code != 200:
         logging.error(f"Failed to fetch data from URL: {url}. Status code: {response.status_code}")
         return pd.DataFrame()  # Return empty DataFrame on error
         
     try:
         xlsData = pd.read_excel(BytesIO(response.content), engine='openpyxl')
         return xlsData
     except Exception as e:
         logging.error(f"Error reading Excel file: {str(e)}")
         return pd.DataFrame()  # Return empty DataFrame on error

def store_data(xlsData):         
    logging.info(f"Available columns in Excel file: {list(xlsData.columns)}")
    for _, row in xlsData.iterrows():
        # Skip row if any required field is empty/NaN
        if pd.isna(row['Number of Orders']) or pd.isna(row['Max Price of Orders ']) or \
           pd.isna(row['Min Price of Orders ']) or pd.isna(row['Average Price of Orders ']) or \
           pd.isna(row['Number of Quotes '])  or \
           pd.isna(row['Start Prices ']) or pd.isna(row['Fixing Prices ']) or \
           pd.isna(row['Open Interest ']):
            logging.info(f"Skipping row with empty values for instrument: {row['Instrument ']}")
            continue
            
        Trade.objects.create(
            day = pd.to_datetime(row['Trade Day']).date(),
            instrument = row['Instrument '],
            number_of_orders = int(row['Number of Orders']),
            max_price_of_orders = float(row['Max Price of Orders ']),
            min_price_of_orders = float(row['Min Price of Orders ']),
            average_price_of_orders = float(row['Average Price of Orders ']),
            number_of_quotes = int(row['Number of Quotes ']),
            number_of_trades = int(0 if pd.isna(row['Number of Trades']) else row['Number of Trades']),
            average_price_of_trades_vwap = float(0 if pd.isna(row['Average Price of Trades (VWAP)']) else row['Average Price of Trades (VWAP)']),
            total_quantity_of_trades = int(0 if pd.isna(row['Total Quantity of Trades ']) else row['Total Quantity of Trades ']),
            start_prices = float(row['Start Prices ']),
            fixing_prices = float(row['Fixing Prices ']),
            open_interest = int(row['Open Interest '])
            )
        logging.info(f"Stored data for instrument: {row['Instrument ']}")