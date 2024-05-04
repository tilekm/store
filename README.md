# Online Store App Pet Project

This is an ecommerce store application built with Django, Celery, Redis, and PostgreSQL. 

## Description

This project is a simple online store with the following features:

- Product listings and details
- Shopping cart 
- Checkout and payments
- Integrated payment gateway
- User accounts and profiles
- Admin portal to manage store inventory and orders

## Technologies

- Python 3.x
- Django 4.1
- Celery - Asynchronous task queue  
- Redis - Broker for Celery
- PostgreSQL 16 - Database

## Installation

To run this project on your local machine:

1. Clone this repository
`git clone https://github.com/tilekm/store.git`


2. Navigate into the project directory
`cd store`


3. Create a virtual environment and activate it
`python3 -m venv env`

`source env/bin/activate`


4. Install dependencies
`pip install -r requirements.txt`


5. Configure postgres database and add credentials to `settings.py` 

6. Run database migrations
`python manage.py migrate`


7. Start Celery worker
`celery -A store worker -l info`

8. Start Redis server
`redis-server`


9. Run the development server
`python manage.py runserver`


The app should now be running at **http://localhost:8000**

## Features Roadmap

Future features planned for implementation:

- Improve recommendations system 
- Add mobile app support
- Internationalize storefront

## Contributing 

Contributions to expand features or fix bugs are welcomed! Please open an issue or submit a pull request detailing your changes.
