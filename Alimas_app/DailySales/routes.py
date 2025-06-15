import json
from flask import Flask, render_template,request,jsonify
from Alimas_app.extensions import db
from Alimas_app.DailySales import bp
from Alimas_app.models.manage import CustomerEntry,SnackEntry
from Alimas_app.utils.common import get_current_utc
from Alimas_app.utils.logwritter import LogWriter 
from Alimas_app.utils.login_requried import login_required
logger = LogWriter()
from datetime import datetime, timedelta


@bp.route('/')
@login_required
def index():
    return render_template("dailysales.html")


@bp.route('/fetch_sales', methods=['POST'])
def fetch_sales():
    data = request.get_json()
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    # Convert to full datetime string boundaries (string format)
    start_datetime_str = start_date_str + " 00:00:00"
    end_datetime_str = end_date_str + " 23:59:59"

    results = CustomerEntry.query.filter(
        CustomerEntry.status == 'Active',
        CustomerEntry.payment_status.in_(['Paid', 'Partial']),
        CustomerEntry.created_on >= start_datetime_str,
        CustomerEntry.created_on <= end_datetime_str
    ).all()

    snack_summary = {}
    total_paid = 0

    for entry in results:
        total_paid += entry.paid_amount
        specials = json.loads(entry.today_special)
        specials = json.loads(specials)
        for item in specials:
            name = item['snackName']
            qty = int(item['quantity'])
            if name in snack_summary:
                snack_summary[name] += qty
            else:
                snack_summary[name] = qty

    response = {
        'snacks': [{'name': k, 'quantity': v} for k, v in snack_summary.items()],
        'total_paid': total_paid
    }

    return jsonify(response)