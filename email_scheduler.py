import json
from decimal import Decimal
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from initiator import app
from processor import PurchaseProcessor

# Function to send email
def send_email(subject, body):
    # Email configuration
    sender_email = "dddpr05@outlook.com"  # Replace with your email
    receiver_email = "dprabha369@gmail.com"  # Replace with manager's email
    password = "12345678@dp"  # Replace with your email password

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, password)
        smtp.send_message(msg)


def decimal_to_float(data):
    if isinstance(data, dict):
        converted_dict = {}
        for key, value in data.items():
            if isinstance(value, dict):
                converted_dict[key] = decimal_to_float(value)
            elif isinstance(value, Decimal):
                converted_dict[key] = float(value)
            else:
                converted_dict[key] = value
        return converted_dict
    elif isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    else:
        return data



# Function to generate bill and send email daily at 10 PM
def send_daily_bill():
    # Generate total sales details
    purchase_processor = PurchaseProcessor()
    total_sales_details = purchase_processor.get_total_sales_daily()

    # Convert total sales details to JSON
    # json_data = json.dumps(decimal_to_float(total_sales_details), indent=4)
    json_data = json.dumps(decimal_to_float(total_sales_details), indent=4)

    # Send email
    subject = "Daily Sales Report"
    body = f"Total Sales Details:\n{json_data}"
    send_email(subject, body)

# Function to generate weekly bill and send email every Saturday at 11 AM
def send_weekly_bill():
    # Generate total sales details for the week
    purchase_processor = PurchaseProcessor()
    total_sales_details_weekly = purchase_processor.get_total_sales_weekly()

    # Convert total sales details to JSON
    json_data = json.dumps(decimal_to_float(total_sales_details_weekly), indent=4)

    # Send emails
    subject = "Weekly Sales Report"
    body = f"Weekly Total Sales Details:\n{json_data}"
    send_email(subject, body)

# Schedule tasks
schedule.every().day.at("22:00").do(send_daily_bill)  # Send daily bill at 10 PM
schedule.every().saturday.at("11:00").do(send_weekly_bill)  # Send weekly bill every Saturday at 11 AM

# Start the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
