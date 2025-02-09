from flask import Flask, render_template,request,jsonify
from config import Config
from models import db, CustomerEntry,SnackEntry
from logwritter import LogWriter 
logger = LogWriter()

app = Flask(__name__)
app.config.from_object(Config) 
db.init_app(app) 


@app.route('/')
def home():
    return render_template("base.html")

@app.route('/user')
def user():
    return render_template("manage.html")
@app.route('/todayspecial')
def todayspecial():
    return render_template("snacks.html")

@app.route('/getdata', methods=['GET'])
def get_data():
    try:
        entries = CustomerEntry.query.all()
        data = []
        
        for entry in entries:
            data.append({
                'id': entry.id,
                'customer_name': entry.customer_name,
                'today_special': entry.today_special,
                'total_amount': entry.total_amount,
                'payment_status': entry.payment_status
            })
        
        return jsonify({'data': data}), 200
    except Exception as e:
        logger.log_exception("app", "getdata", e)
        return jsonify({'error': str(e)}), 500

@app.route('/savedata', methods=['POST'])
def save_data():
    customer_name = request.form.get('customerName')
    today_special = request.form.get('todaySpecial')
    total_amount = request.form.get('totalAmount')
    payment_status = request.form.get('paymentStatus')

    if not customer_name or not today_special or not total_amount or not payment_status:
        return jsonify({'error': 'All fields are required!'}), 400

    try:
        new_entry = CustomerEntry(
            customer_name=customer_name,
            today_special=today_special,
            total_amount=float(total_amount), 
            payment_status=payment_status
        )

      
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({'message': 'Special saved successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "savedata", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/updatecustomer', methods=['POST'])
def update_customer():
    try:
        # Get the customer data from the request body
        customer_id = request.form.get('id')
        customer_name = request.form.get('customerName')
        today_special = request.form.get('todaySpecial')
        total_amount = request.form.get('totalAmount')
        payment_status = request.form.get('paymentStatus')

        # Find the customer entry by ID
        entry = CustomerEntry.query.get(customer_id)
        if entry:
            entry.customer_name = customer_name
            entry.today_special = today_special
            entry.total_amount = float(total_amount)
            entry.payment_status = payment_status

            db.session.commit()

            return jsonify({'message': 'Customer updated successfully!'}), 200
        else:
            return jsonify({'error': 'Customer not found!'}), 404
    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "updatecustomer", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/deletecustomer', methods=['DELETE'])
def delete_customer():
    try:
        data = request.get_json()  # Get the JSON data from the request body
        customer_id = data.get('id')  # Extract the id
        
        if not customer_id:
            return jsonify({'error': 'Customer ID is required!'}), 400
        
        # Find the customer entry by id
        entry = CustomerEntry.query.get(customer_id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({'message': 'Customer deleted successfully!'}), 200
        else:
            return jsonify({'error': 'Customer not found!'}), 404
    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "deletecustomer", e)
        return jsonify({'error': str(e)}), 500
    
# save snacks

@app.route('/getsnack', methods=['GET'])
def get_snacks():
    try:
        entries = SnackEntry.query.all()
        data = []
        
        for entry in entries:
            data.append({
                'id': entry.id,
                'snacks_name': entry.snacks_name,
                'snack_price': entry.snack_price,
                'today_special': entry.today_special,
            })
        
        return jsonify({'data': data}), 200
    except Exception as e:
        logger.log_exception("app", "getsnacks", e)
        return jsonify({'error': str(e)}), 500 

@app.route('/savesnack', methods=['POST'])
def save_snack():
    snack_name = request.form.get('snackName')
    snack_price = request.form.get('snackPrice')

    if not snack_name or not snack_price:
        return jsonify({'error': 'Snack Name and Price are required!'}), 400

    try:
        new_snack = SnackEntry(
            snacks_name=snack_name,
            snack_price=float(snack_price),
            today_special=False
        )

        db.session.add(new_snack)
        db.session.commit()

        return jsonify({'message': 'Snack saved successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "save_data", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/updatesnack', methods=['PUT'])
def update_snack():
    try:
        data = request.get_json()
        snack_id = data.get('id')
        snack_name = data.get('snackName')
        snack_price = data.get('snackPrice')

        if not snack_id or not snack_name or not snack_price:
            return jsonify({'error': 'Snack ID, Name, and Price are required!'}), 400

        snack_entry = SnackEntry.query.get(snack_id)  # SQLAlchemy 2.x
        if not snack_entry:
            return jsonify({'error': 'Snack not found!'}), 404

        # Update values
        snack_entry.snacks_name = snack_name
        snack_entry.snack_price = float(snack_price)

        db.session.commit()
        return jsonify({'message': 'Snack updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "update_snack", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/deletesnack', methods=['DELETE'])
def delete_snack():
    try:
        data = request.get_json()
        id = data.get('id')
        
        if not id:
            return jsonify({'error': 'Snack ID is required!'}), 400
        
        entry = SnackEntry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({'message': 'Snack deleted successfully!'}), 200
        else:
            return jsonify({'error': 'Snack not found!'}), 404
    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "deletesnack", e)
        return jsonify({'error': str(e)}), 500

with app.app_context():
    db.create_all() 

if __name__ == "__main__":
    app.run(debug=True)
