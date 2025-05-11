# myapp/tasks.py

from celery import shared_task
from datetime import datetime
from celery.schedules import crontab
from Synertics.celery import app
from django.core.mail import send_mail
from django.conf import settings

from io import BytesIO
import requests
import pandas as pd
from .models import Trade

import logging
import traceback
logging.basicConfig(level=logging.INFO)

def send_error_notification(subject, error_message):
    try:
        send_mail(
            subject=subject,
            message=error_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        logging.info(f"Error notification sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send error notification: {str(e)}")

@shared_task(name='daily_scrape')
def daily_scrape():
    current_time = datetime.now().strftime("%Y%m%d")
    logging.info(f"Starting daily scrape at {current_time}")
    
    url=f"https://www.enexgroup.gr/documents/20126/314344/{current_time}_DER_DOL_EN_v01.xlsx"
    logging.info(f"Fetching data from URL: {url}")

    try:
        xlsData = fetch_url(url)
        if xlsData.empty:
            error_msg = f"No data found for the date: {current_time}"
            logging.error(error_msg)
            send_error_notification(
                f"Scraping Error - No Data Found ({current_time})",
                f"Failed to find data for date {current_time}.\nURL: {url}"
            )
            return f"No data found for {current_time}"

        logging.info(f"Data fetched successfully for the date: {current_time}")
        store_data(xlsData)
        return f"Daily task completed at {current_time}"

    except Exception as e:
        error_msg = f"Unexpected error during scraping: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        send_error_notification(
            f"Scraping Error - Unexpected Error ({current_time})",
            f"An unexpected error occurred during scraping:\n\n{error_msg}\n\nURL: {url}"
        )
        raise  # Re-raise the exception for Celery to handle

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
    
    for _, row in xlsData.iterrows():
       
            
        Trade.objects.create(
            day = pd.to_datetime(row['Trade Day']).date(),
            instrument = row['Instrument '],
            number_of_orders = int(0 if pd.isna(row['Number of Orders']) else row['Number of Orders']),
            max_price_of_orders = float(0 if pd.isna(row['Max Price of Orders ']) else row['Max Price of Orders ']),
            min_price_of_orders = float(0 if pd.isna(row['Min Price of Orders ']) else row['Min Price of Orders ']),
            average_price_of_orders = float(0 if pd.isna(row['Average Price of Orders ']) else row['Average Price of Orders ']),
            number_of_quotes = int(0 if pd.isna(row['Number of Quotes ']) else row['Number of Quotes ']),
            number_of_trades = int(0 if pd.isna(row['Number of Trades']) else row['Number of Trades']),
            average_price_of_trades_vwap = float(0 if pd.isna(row['Average Price of Trades (VWAP)']) else row['Average Price of Trades (VWAP)']),
            total_quantity_of_trades = int(0 if pd.isna(row['Total Quantity of Trades ']) else row['Total Quantity of Trades ']),
            start_prices = float(0 if pd.isna(row['Start Prices ']) else row['Start Prices ']),
            fixing_prices = float(0 if pd.isna(row['Fixing Prices ']) else row['Fixing Prices ']),
            open_interest = int(0 if pd.isna(row['Open Interest ']) else row['Open Interest '])
            )
        logging.info(f"Stored data for instrument: {row['Instrument ']}")