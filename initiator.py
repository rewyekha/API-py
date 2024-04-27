from flask import Flask, jsonify, request
from processor import UserProcessor, PurchaseProcessor, ItemProcessor, StoreUserProcessor

import datetime

app = Flask(__name__)

# User Signup endpoint
import bcrypt


# User signup endpoint
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if data:
            # Extract password from the request data
            password = data.get('Password')

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Replace plain password with hashed password in the request data
            data['Password'] = hashed_password

            # Process signup
            user_processor = UserProcessor()
            response = user_processor.signup(data)
            return jsonify(response)
        else:
            return jsonify({'error': 'No data provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/store/signup', methods=['POST'])
def store_signup():
    data = request.get_json()
    store_user_processor = StoreUserProcessor()  # Update to use StoreUserProcessor
    response = store_user_processor.store_signup(data)  # Update to use signup method for store users
    return jsonify(response)


# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if data:
            email = data.get('Email_ID')
            password = data.get('Password')

            # Fetch user data from the database based on the provided email
            user_processor = UserProcessor()
            user_data = user_processor.get_user_by_email(email)

            if user_data:
                # Retrieve hashed password from the user data
                hashed_password_from_db = user_data.get('Password')

                # Check if the provided password matches the hashed password from the database
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
                    # Passwords match, login successful
                    return jsonify({'message': 'Login successful'})
                else:
                    # Passwords don't match, login failed
                    return jsonify({'error': 'Invalid credentials'}), 401
            else:
                # User not found with the provided email
                return jsonify({'error': 'User not found'}), 404
        else:
            # No data provided in the request
            return jsonify({'error': 'No data provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/store/login', methods=['POST'])
def store_login():
    data = request.get_json()
    store_user_processor = StoreUserProcessor()
    response = store_user_processor.store_login(data)
    return jsonify(response)

# Purchase endpoint
@app.route('/purchase', methods=['POST'])
def purchase():
    data = request.get_json()
    purchase_processor = PurchaseProcessor()
    response = purchase_processor.purchase(data)
    return jsonify(response)

# Total number of items purchased in the given date range endpoint
@app.route('/total_items_purchased', methods=['GET'])
def total_items_purchased():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if start_date and end_date:
            purchase_processor = PurchaseProcessor()
            total_items = purchase_processor.get_total_items_purchased(start_date, end_date)
            return jsonify({'total_items': total_items})
        else:
            return jsonify({'error': 'Start date and end date are required'})
    except Exception as e:
        return jsonify({'error': str(e)})

# List users who have purchased for more than Rs 1000 in a day endpoint
@app.route('/high_value_users', methods=['GET'])
def high_value_users():
    purchase_processor = PurchaseProcessor()
    response = purchase_processor.high_value_users()
    return jsonify(response)

# Total sales in the amount of product shampoo in the last 7 days endpoint
@app.route('/total_shampoo_sales_last_week', methods=['GET'])
def total_shampoo_sales_last_week():
    purchase_processor = PurchaseProcessor()
    response = purchase_processor.total_shampoo_sales_last_week()
    return jsonify(response)


# Add item endpoint
@app.route('/add_item/<string:designation>', methods=['POST'])
def add_item(designation):
    try:
        if designation == 'manager':  # Check if the user is a manager
            data = request.get_json()
            if data:  # Check if data is not empty
                if isinstance(data, list):  # Check if data is a list of items
                    item_processor = ItemProcessor()
                    for item in data:
                        item_processor.add_item(item)
                    return jsonify({'message': 'Items added successfully'})
                else:  # If data is a single item
                    item_processor = ItemProcessor()
                    item_processor.add_item(data)
                    return jsonify({'message': 'Item added successfully'})
            else:
                return jsonify({'error': 'No data provided'})
        else:
            return jsonify({'error': 'Access denied. Only managers can perform this operation.'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete item endpoint
@app.route('/delete_item/<int:item_id>/<string:designation>', methods=['DELETE'])
def delete_item(item_id, designation):
    try:
        if designation == 'manager':  # Check if the user is a manager
            item_processor = ItemProcessor()
            response = item_processor.delete_item(item_id)
            return jsonify(response)
        else:
            return jsonify({'error': 'Access denied. Only managers can perform this operation.'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update item rate endpoint
@app.route('/update_item_rate/<int:item_id>/<string:designation>', methods=['PUT'])
def update_item_rate(item_id, designation):
    try:
        if designation == 'manager':  # Check if the user is a manager
            new_rate = request.get_json()['new_rate']
            item_processor = ItemProcessor()
            response = item_processor.update_item_rate(item_id, new_rate)
            return jsonify(response)
        else:
            return jsonify({'error': 'Access denied. Only managers can perform this operation.'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=False)
