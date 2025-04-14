from flask import Flask, render_template,request,jsonify
from Alimas_app.extensions import db
from Alimas_app.customersdue import bp
from Alimas_app.models.manage import CustomerEntry
from Alimas_app.utils.logwritter import LogWriter 
logger = LogWriter()


@bp.route('/')
def index():
    return render_template("customerdue.html")


@bp.route('/getduedata', methods=['GET'])
def get_data():
    try:
        entries = CustomerEntry.query.filter(
            CustomerEntry.payment_status.in_(['Unpaid', 'Partial'])
        ).all()
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