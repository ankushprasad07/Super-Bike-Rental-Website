# Super-Bike-Rental-Website

## Overview
The **Super Bike Rental Website** is an online platform where users can rent superbikes for a specified period. The website allows customers to browse available bikes, view details, book their rentals, and make payments online. It also includes an admin panel for managing bookings, bike details, and payments.

## Features
- **User Registration and Login**: Customers can register and log in to access booking functionalities.
- **Browse Bikes**: Customers can browse available bikes along with their details like price, specifications, and images.
- **Booking System**: Customers can select bikes, choose rental dates, and book bikes.
- **Payment System**: Customers can pay using credit cards for bike rental and security deposits.
- **Booking History**: Users can view their past bookings and statuses.
- **Admin Panel**: Admin users can manage bookings, bikes, and view analytics.
  
## Technologies Used
- **Backend**: Django
- **Frontend**: HTML, CSS (Bootstrap or Tailwind), JavaScript
- **Database**: SQLite (or any other preferred database like PostgreSQL)
- **Payment Gateway**: Custom implementation or third-party service for processing payments (like Stripe or Razorpay).
- **Version Control**: Git & GitHub

## Installation

To run the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/ankushprasad07/Super-Bike-Rental-Website.git
   
Navigate to the project folder:
cd superbike_rental

Create a virtual environment and activate it:
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

Install the dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py makemigrations
python manage.py migrate

Run the development server:
python manage.py runserver
Now, you should be able to access the project at http://127.0.0.1:8000/ in your browser.
