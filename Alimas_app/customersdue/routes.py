from flask import Flask, render_template,request,jsonify,send_file,current_app
from Alimas_app.extensions import db
from Alimas_app.customersdue import bp
from Alimas_app.models.manage import CustomerEntry
from Alimas_app.utils.logwritter import LogWriter 
from fpdf import FPDF
import json,os
import io
from datetime import datetime
pdf = FPDF()
logger = LogWriter()
buffer = io.BytesIO()


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

@bp.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    try:
        customer_id = request.form.get('customer_id')
        if not customer_id:
            return jsonify({'error': 'Missing customer_id'}), 400

        entry = CustomerEntry.query.get(int(customer_id))
        if not entry:
            return jsonify({'error': 'Customer not found'}), 404

        snack_item = json.loads(entry.today_special)

        print(f"Raw today_special: {snack_item}")

        try:
            snack_items = json.loads(snack_item)
            print(snack_items) 
        except json.JSONDecodeError as e:
            print({'error': f'Invalid JSON format in today_special: {str(e)}'})

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        font_path_regular = os.path.join(current_app.root_path, 'customersdue', 'DejaVuSans.ttf')
        font_path_bold = os.path.join(current_app.root_path, 'customersdue', 'DejaVuSans-Bold.ttf')

        pdf.add_font('DejaVu', '', font_path_regular, uni=True)
        pdf.add_font('DejaVu', 'B', font_path_bold, uni=True)

        pdf.set_font('DejaVu', '', 14) 

        logo_path = os.path.join(current_app.root_path, 'static','images','logos','logo.png')
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=30)

        pdf.set_xy(50, 10)
        pdf.set_font_size(18)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(100, 10, txt="Aalimas Thanthoori Chai", ln=True)
        pdf.set_font_size(12)
        pdf.set_x(50)
        pdf.cell(100, 8, txt="Aalimas Tandoori Chai, Old Fish Market Street, Chitharkottai-623513", ln=True)
        pdf.set_x(50)
        pdf.cell(100, 8, txt="Phone: +91-9659408358", ln=True)
        pdf.ln(20)

        pdf.set_text_color(0, 0, 0)
        pdf.cell(100, 8, txt=f"Invoice for: {entry.customer_name}", ln=True)
        pdf.cell(100, 8, txt=f"Invoice ID: {entry.customer_name}-{entry.id}", ln=True)
        pdf.cell(100, 8, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        if entry.payment_status == "Partial":
            pdf.cell(100, 8, txt="Status: Partially Paid", ln=True)
        elif entry.payment_status == "Unpaid":
            pdf.cell(100, 8, txt="Status: Un Paid", ln=True)
        pdf.ln(5)

        pdf.set_fill_color(230, 230, 230)
        pdf.set_font(style='B')
        pdf.cell(10, 10, "No", 1, 0, 'C', True)
        pdf.cell(70, 10, "Item", 1, 0, 'C', True)
        pdf.cell(30, 10, "Qty", 1, 0, 'C', True)
        pdf.cell(30, 10, "Price", 1, 0, 'C', True)
        pdf.cell(40, 10, "Total", 1, 1, 'C', True)

        pdf.set_font(style='')
        for i, item in enumerate(snack_items, 1):
            total = item["quantity"] * item["price"]
            pdf.cell(10, 10, str(i), 1, 0, 'C')
            pdf.cell(70, 10, item["snackName"], 1)
            pdf.cell(30, 10, str(item["quantity"]), 1, 0, 'C')
            pdf.cell(30, 10, f"₹{item['price']}", 1, 0, 'C')
            pdf.cell(40, 10, f"₹{total}", 1, 1, 'C')

        pdf.ln(5)

        balance = entry.total_amount - entry.paid_amount
        pdf.set_font(style='B')
        pdf.cell(180, 10, f"Total Amount: ₹{entry.total_amount}", ln=True, align='R')
        pdf.cell(180, 10, f"Paid Amount: ₹{entry.paid_amount}", ln=True, align='R')
        pdf.cell(180, 10, f"Balance: ₹{balance}", ln=True, align='R')

        pdf.ln(10)
        pdf.set_font(style='')
        pdf.cell(200, 10, txt="Thank you for choosing Aalimas Thanthoori Chai!", ln=True, align='C')

        save_dir = os.path.join(current_app.root_path, 'static', 'media')
        os.makedirs(save_dir, exist_ok=True)
        local_path = os.path.join(save_dir, f'invoice_{entry.id}.pdf')
        pdf.output(local_path)

        buffer = io.BytesIO()
        pdf.output(buffer)
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, mimetype='application/pdf',
                         download_name=f'invoice_{entry.id}.pdf')

    except Exception as e:
        print("Invoice Error:", e)
        return jsonify({'error': str(e)}), 500
