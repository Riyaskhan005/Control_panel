import json
from flask import Flask, render_template,request,jsonify
from Alimas_app.extensions import db
from Alimas_app.managecustomers import bp
from Alimas_app.models.manage import CustomerEntry,SnackEntry
from Alimas_app.utils.logwritter import LogWriter 
logger = LogWriter()


@bp.route('/')
def index():
    return render_template("manage.html")

@bp.route('/getdata', methods=['GET'])
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
                'payment_status': entry.payment_status,
                'paid_amount': entry.paid_amount
            })
        
        return jsonify({'data': data}), 200
    except Exception as e:
        logger.log_exception("app", "getdata", e)
        return jsonify({'error': str(e)}), 500

@bp.route('/savedata', methods=['POST'])
def save_data():
    customer_name = request.form.get('customerName')
    today_special = request.form.get('todaySpecial')
    total_amount = request.form.get('totalAmount')
    payment_status = request.form.get('paymentStatus')
    paid_amount = request.form.get('paidAmount')

    today_special_json = json.dumps(today_special)

    if not customer_name or not today_special or not total_amount or not payment_status:
        return jsonify({'error': 'All fields are required!'}), 400

    try:
        new_entry = CustomerEntry(
            customer_name=customer_name,
            today_special=today_special_json,
            total_amount=float(total_amount),
            paid_amount=paid_amount,  
            payment_status=payment_status
        )

      
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({'message': 'Special saved successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "savedata", e)
        return jsonify({'error': str(e)}), 500
    
@bp.route('/updatecustomer', methods=['POST'])
def update_customer():
    try:
        # Get the customer data from the request body
        customer_id = request.form.get('id')
        customer_name = request.form.get('customerName')
        today_special = request.form.get('todaySpecial')
        total_amount = request.form.get('totalAmount')
        payment_status = request.form.get('paymentStatus')
        paid_amount = request.form.get('paidAmount')
        print(paid_amount)

        # Find the customer entry by ID
        entry = CustomerEntry.query.get(customer_id)
        if entry:
            entry.customer_name = customer_name
            entry.today_special = today_special
            entry.total_amount = float(total_amount)
            entry.paid_amount =float(paid_amount)
            entry.payment_status = payment_status

            db.session.commit()

            return jsonify({'message': 'Customer updated successfully!'}), 200
        else:
            return jsonify({'error': 'Customer not found!'}), 404
    except Exception as e:
        db.session.rollback()
        logger.log_exception("app", "updatecustomer", e)
        return jsonify({'error': str(e)}), 500
    
@bp.route('/deletecustomer', methods=['DELETE'])
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
    


@bp.route('/getsnack', methods=['GET'])
def get_snacks():
    try:
        entries = SnackEntry.query.filter_by(status="Active", today_special="true").all()
        
        data = []
        for entry in entries:
            data.append({
                'id': entry.id,
                'snacks_name': entry.snacks_name,
                'snack_price': entry.snack_price,
            })
        
        return jsonify({'data': data}), 200
    except Exception as e:
        logger.log_exception("app", "getsnacks", e)
        return jsonify({'error': str(e)}), 500