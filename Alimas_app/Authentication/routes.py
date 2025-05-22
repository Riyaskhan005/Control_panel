from flask import Flask, render_template,request,jsonify,send_file,current_app,session
from Alimas_app.extensions import db
from Alimas_app.Authentication import bp
from Alimas_app.models.manage import Users
from Alimas_app.utils.logwritter import LogWriter 
from fpdf import FPDF
import json,os
import io
from datetime import datetime

logger = LogWriter()


@bp.route('/')
def index():
    return render_template("login.html")


@bp.route('/login', methods=['POST'])
def login():
    return_msg= {}
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = Users.query.filter_by(Email=email, status='Active').first()

        if user and user.Password == password:
            session['user_id'] = user.id
            session['user_name'] = f"{user.First_name} {user.Last_name}"
            session['email'] = user.Email
            
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'first_name': user.First_name,
                    'last_name': user.Last_name,
                    'email': user.Email
                }
            }), 200
        else:
            return jsonify({'status': 'fail', 'message': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
