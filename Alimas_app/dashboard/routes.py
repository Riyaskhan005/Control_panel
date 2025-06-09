from flask import Flask, render_template,request,jsonify
from Alimas_app.extensions import db
from Alimas_app.dashboard import bp
from Alimas_app.models.manage import CustomerEntry, SnackEntry
from Alimas_app.utils.logwritter import LogWriter 
from Alimas_app.utils.login_requried import login_required
logger = LogWriter()


@bp.route('/')
@login_required
def index():
    return render_template("dashboard.html")

@bp.route("/load_dashboard")
def load_dashboard():
    try:
        active_customers = CustomerEntry.query.filter_by(status="Active")
        count = active_customers.count()
        credited_amount = (
            db.session.query(db.func.sum(CustomerEntry.paid_amount))
            .filter(CustomerEntry.payment_status.in_(["Paid", "Partial"]),
                    CustomerEntry.status == "Active")
            .scalar()
        )
        credited_amount = credited_amount or 0

        return jsonify({
            "count": count,
            "credited_amount": round(credited_amount, 2)
        })
    except Exception as e:
        logger.log_exception("app", "getdata", e)

    
@bp.route('/availabel_snack', methods=['GET'])
def availabel_snack():
    try:
        entries = SnackEntry.query.filter_by(today_special="true").all()
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
