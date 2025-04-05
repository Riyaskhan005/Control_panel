from flask import Flask, render_template,request,jsonify
from Alimas_app.extensions import db
from Alimas_app.managesnacks import bp
from Alimas_app.models.manage import SnackEntry
from Alimas_app.utils.logwritter import LogWriter 
logger = LogWriter()


@bp.route('/')
def index():
    return render_template("snacks.html")


@bp.route('/getsnack', methods=['GET'])
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

@bp.route('/savesnack', methods=['POST'])
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
    
@bp.route('/updatesnack', methods=['PUT'])
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
    
@bp.route('/deletesnack', methods=['DELETE'])
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
