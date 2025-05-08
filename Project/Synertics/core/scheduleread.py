# import time
# import schedule

# def job():
#     df = get_xlsx_data("https://example.com/data.xlsx")
#     df.to_csv("daily_data.csv", index=False)
#     print("Scraped and saved data.")

# schedule.every().day.at("08:00").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(60)
