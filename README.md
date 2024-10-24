# Seahawk Restaurant Management System

The Seahawk Restaurant Management System is designed to address the challenges of improper meat inventory management and enhance the customer experience through a sophisticated reservation system. This project includes two main modules: a **Smart Inventory Module** and a **Smart Reservation Module**.

## Features

### Smart Inventory Module
- **Expiration Tracking**: Monitors expiration dates of meat inventories (beef, pork, and chicken) and notifies inventory staff before items expire.
- **Market Price Monitoring**: Tracks current market prices for high-quality meats and alerts staff when prices drop below the 5-day moving average for timely ordering.
- **Low Stock Alerts**: Notifies staff when stock levels fall below a certain threshold.
- **Predictive Analytics**: Predicts potential meat shortages based on historical purchase data, providing proactive notifications.
- **Detailed Inventory Data**: Allows inventory staff to view comprehensive inventory information.

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
- MySQL 8.x
- MySQL client (`mysqlclient`)

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

Make sure `mysqlclient` is in `requirements.txt`. If not, install it manually:

```bash
pip install mysqlclient
```




### 7. Run the development server

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

## License

This project is licensed under the MIT License.
