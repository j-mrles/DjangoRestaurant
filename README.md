# Seahawk Restaurant Management System

The Seahawk Restaurant Management System is designed to address the challenges of improper meat inventory management and enhance the customer experience through a sophisticated reservation system. This project includes a main module: **Smart Reservation Module**.

## Features

### Smart Reservation Module
- **Seating Capacity**: Manages a seating capacity of 300, with the option to expand to 400 seats.
- **Reservation Management**: Customers can reserve up to 200 seats in a single reservation.
- **Visual Seating Layout**: Displays real-time status of each table (reserved, occupied, available) for easy management.
- **Reservation Modifications**: Customers can make, update, or cancel reservations.
- **Automatic Cancellation**: Reservations are automatically canceled if customers do not arrive within 30 minutes of the scheduled time.
- **Special Accommodations**: Customers can request specific needs (e.g., wheelchair accessibility) and save seating preferences for future bookings.
- **Estimated Wait Times**: Provides estimated wait times for walk-in customers.

## Requirements

Before you start, ensure you have the following installed:

- Python 3.10 or higher
- Django 4.x


## Installation

### 1. Clone the repository

First, clone this repository from GitHub:

```bash
git clone https://github.com/yourusername/seahawk-restaurant-management.git
cd seahawk-restaurant-management
```

### 2. Set up a virtual environment

It’s recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate    # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies (DO NOT TOUCH DB YET)

Install the required Python packages:

```bash
pip install -r requirements.txt
```






### 4. Run the development server

Now you can run the development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to access the application.

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin` to manage inventory and reservations.
- Use the reservation system to book tables, manage customer seating preferences, and monitor wait times.

## Contributing

If you want to contribute to this project:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.


