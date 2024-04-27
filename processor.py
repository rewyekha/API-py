from datetime import datetime, timedelta

from database import Database

class UserProcessor:
    def signup(self, data):
        db = Database()
        query = "INSERT INTO User_details (First_Name, Last_Name, Age, Sex, Contact_Number, Email_ID, Password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        db.execute_query(query, (data['First_Name'], data['Last_Name'], data['Age'], data['Sex'], data['Contact_Number'], data['Email_ID'], data['Password']))
        db.commit()
        db.close_connection()
        return {'message': 'User signed up successfully'}

    def login(self, data):
        db = Database()
        query = "SELECT * FROM User_details WHERE Email_ID = %s AND Password = %s"
        db.execute_query(query, (data['Email_ID'], data['Password']))
        user = db.fetch_one()
        db.close_connection()
        if user:
            return {'message': 'Login successful', 'user_id': user[0]}
        else:
            return {'message': 'Invalid credentials'}

    def get_user_by_email(self, email):
        db = Database()
        query = "SELECT * FROM User_details WHERE Email_ID = %s"
        db.execute_query(query, (email,))
        user_data_row = db.fetch_one()
        db.close_connection()

        # Convert row data to dictionary
        user_data = {}
        if user_data_row:
            user_data['User_id'] = user_data_row[0]
            user_data['First_Name'] = user_data_row[1]
            user_data['Last_Name'] = user_data_row[2]
            user_data['Age'] = user_data_row[3]
            user_data['Sex'] = user_data_row[4]
            user_data['Contact_Number'] = user_data_row[5]
            user_data['Email_ID'] = user_data_row[6]
            user_data['Password'] = user_data_row[7]

        return user_data

class StoreUserProcessor:
    def store_signup(self, data):
        db = Database()
        query = "INSERT INTO Store_user (First_Name, Last_Name, Age, Sex, Contact_Number, Email_ID, Password, Designation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        db.execute_query(query, (data['First_Name'], data['Last_Name'], data['Age'], data['Sex'], data['Contact_Number'], data['Email_ID'], data['Password'], data['Designation']))
        db.commit()
        db.close_connection()
        return {'message': 'Store user signed up successfully'}

    def store_login(self, data):
        db = Database()
        query = "SELECT * FROM Store_user WHERE Email_ID = %s AND Password = %s"
        db.execute_query(query, (data['Email_ID'], data['Password']))
        user = db.fetch_one()
        db.close_connection()
        if user:
            return {'message': 'Login successful', 'user_id': user[0]}
        else:
            return {'message': 'Invalid credentials'}

class PurchaseProcessor:
    def purchase(self, data):
        db = Database()
        query = "INSERT INTO Purchase (User_id, Item, Quantity, Rate, Date_of_purchase) VALUES (%s, %s, %s, %s, %s)"
        db.execute_query(query, (data['User_id'], data['Item'], data['Quantity'], data['Rate'], data['Date_of_purchase']))
        db.commit()
        db.close_connection()
        return {'message': 'Purchase recorded successfully'}

    def get_total_items_purchased(self, start_date, end_date):
        db = Database()
        query = """
            SELECT SUM(Quantity) AS total_items
            FROM Purchase
            WHERE Date_of_purchase >= %s AND Date_of_purchase <= %s
        """
        db.execute_query(query, (start_date, end_date))
        total_items = db.fetch_one()[0]
        db.close_connection()
        return total_items

    def high_value_users(self):
        db = Database()
        query = """
            SELECT U.First_Name, U.Last_Name, SUM(P.Quantity * P.Rate) AS Total_amount
            FROM Purchase P
            INNER JOIN User_details U ON P.User_id = U.User_id
            GROUP BY P.User_id
            HAVING Total_amount > 1000
        """
        db.execute_query(query)
        high_value_users = db.fetch_all()
        db.close_connection()
        return [{'First_Name': user[0], 'Last_Name': user[1], 'Total_purchase_amount': user[2]} for user in
                high_value_users]

    def total_shampoo_sales_last_week(self):
        db = Database()
        query = "SELECT SUM(Quantity*Rate) FROM Purchase WHERE Item = 'Shampoo' AND Date_of_purchase BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW()"
        db.execute_query(query)
        total_sales = db.fetch_one()[0]
        db.close_connection()
        return {'total_shampoo_sales_last_week': total_sales}


    def get_total_sales_daily(self):
        # Calculate the start and end timestamps for the current day
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        db = Database()
        query = "SELECT Item, SUM(Quantity) AS Total_QTY, SUM(Quantity*Rate) AS Total_Amount FROM Purchase WHERE Date_of_purchase BETWEEN %s AND %s GROUP BY Item"
        db.execute_query(query, (today_start, today_end))
        total_sales_daily = db.fetch_all()
        db.close_connection()

        # Construct JSON dictionary
        total_sales_details = {}
        for row in total_sales_daily:
            item = row[0]
            qty = row[1]
            amount = row[2]
            total_sales_details[item] = {'QTY': qty, 'Amount': amount}

        return total_sales_details

    def get_total_sales_weekly(self):
        # Calculate the start and end timestamps for the current week (from Monday to Sunday)
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)

        db = Database()
        query = "SELECT Item, SUM(Quantity) AS Total_QTY, SUM(Quantity*Rate) AS Total_Amount FROM Purchase WHERE Date_of_purchase BETWEEN %s AND %s GROUP BY Item"
        db.execute_query(query, (start_of_week, end_of_week))
        total_sales_weekly = db.fetch_all()
        db.close_connection()

        # Construct JSON dictionary
        total_sales_details_weekly = {}
        for row in total_sales_weekly:
            item = row[0]
            qty = row[1]
            amount = row[2]
            total_sales_details_weekly[item] = {'QTY': qty, 'Amount': amount}

        return total_sales_details_weekly


class ItemProcessor:
    def add_item(self, data):
        db = Database()
        query = "INSERT INTO Products (Product_name, Rate, Stock) VALUES (%s, %s, %s)"
        db.execute_query(query, (data['Product_name'], data['Rate'], data['Stock']))
        db.commit()
        db.close_connection()
        return {'message': 'Item added successfully'}

    def delete_item(self, item_id):
        db = Database()
        query = "DELETE FROM Products WHERE Product_id = %s"
        db.execute_query(query, (item_id,))
        db.commit()
        db.close_connection()
        return {'message': 'Item deleted successfully'}

    def update_item_rate(self, item_id, new_rate):
        db = Database()
        query = "UPDATE Products SET Rate = %s WHERE Product_id = %s"
        db.execute_query(query, (new_rate, item_id))
        db.commit()
        db.close_connection()
        return {'message': 'Item rate updated successfully'}
