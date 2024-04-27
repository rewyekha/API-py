# Supermarket Backend Application 
- This project is a backend application for managing stocks, sales, and user purchases in a supermarket. It provides a REST API for various functionalities such as user signup, login, purchase tracking, item management, and more.

## Features
- User Signup: Allows users to register with their details.
- Login: Authenticate users and provide access to their accounts.
- Purchase Tracking: Record individual purchase history for each user.
- Item Management: Add, delete, and update items in the product inventory.
- Sales Reporting: Generate daily and weekly sales reports and send them via email.

## Technologies Used:
- Python Flask: Backend framework for building REST APIs.
- MySQL Database: Database management system for storing data.
- Schedule: Python library for scheduling tasks.
- SMTP (Simple Mail Transfer Protocol): Protocol for sending emails.

## Set up the database:
- Run the provided MySQL script in SQL_queries.txt file to create the necessary tables

## Run the application:
- python initiator.py
- Access the API endpoints using a tool like Postman.
## Usage
- Use Postman or any API testing tool to interact with the endpoints.
- Register users using the /signup endpoint.
- Login with registered user credentials using the /login endpoint.
- Perform various actions such as purchasing items, managing products, and generating reports.
- Run the email_scheduler.py file for bill generation.

## API Endpoints
- /signup: User signup endpoint.
- /login: User login endpoint.
- /store/signup: store user signup endpoint.
- /store/login: store user login endpoint.
- /purchase: Record user purchases.
- /add_item/<string:designation>: Add items to the product inventory.
- /delete_item/<int:item_id>/<string:designation>: Delete items from the product inventory.
- /update_item_rate/<int:item_id>/<string:designation>: Update the rate of an item.
- /total_items_purchased: Get total items purchased in a given date range.
- /high_value_users: Get users who purchased items worth more than Rs 1000 in a day.
- /total_sales_shampoo_last_7_days: Get the total sales amount of shampoo in the last 7 days.
