# Synertics Project

A Django-based web application developed for a short internship challenge at Synertics, a German company providing market analytics over renewable energy.

## Description

Synertics is a platform that automates the data scraping of Greek electricity futures prices, processes the data, and provides up-to-date insights through a modern web interface and a comprehensive REST API. Built using Django, PostgreSQL, Celery, and Redis, the system handles background scheduled tasks, email error notifications, and provides responsive visualization of market trends via Chart.js. Detailed project documentation can be found in the repository file Synertics_Project_Documentation.pdf.

## Getting Started

### Dependencies

* Docker: The system needs Docker installed to run, as the application is built within isolated and reproducible Docker containers.

### Installing

* Clone or download the repository to your local machine (available as a zip file or Git repository).
* Open Synertics/settings.py and update the email configuration fields with your credentials to enable error notifications for web scraping (Only needed for email notifications, system runs without this).

### Executing program

* Open your terminal in the root project directory.
* Run the following command to build and start all containers: docker-compose up --build.
* Access the web interface and routes:
```
-Dashboard: Visit http://localhost:8000/ to view the 7-day market trends chart.
-Admin Panel: Visit http://localhost:8000/admin/ for the Django admin interface.
-Manual Scraper: Visit http://localhost:8000/call_scraper/ to trigger the daily scraper function manually.
```

## Help
* If the web scraping process fails, check the application logs located at logs/scrape.log for event details.
* Ensure your Gmail app password is correctly configured in Synertics/settings.py if email alerts are not sending.

## Authors

André Rodrigues
rodrigues.n.andre46@gmail.com
