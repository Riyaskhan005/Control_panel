import base64,os
from flask import Flask, current_app, render_template,request,jsonify, session
from Alimas_app.extensions import db
from Alimas_app.settings import bp
from Alimas_app.models.manage import SnackEntry, Users
from Alimas_app.utils.logwritter import LogWriter 
from Alimas_app.utils.login_requried import login_required
logger = LogWriter()


@bp.route('/')
@login_required
def index():
    return render_template("settings.html")

@bp.route('upload_profile_image', methods=['POST'])
def upload_profile_image():
    file = request.files.get('profileImage')
    user_id = session.get('user_id')
    
    static_folder = os.path.join(current_app.root_path, 'static')
    upload_path = os.path.join(static_folder, 'uploads')
    os.makedirs(upload_path, exist_ok=True)

    filename = file.filename
    unique_filename = f"user_{user_id}_{filename}"
    save_path = os.path.join(upload_path, unique_filename)
    file.save(save_path)

    # Build relative path to store
    relative_path = f"/static/uploads/{unique_filename}"

    # Update DB and session
    user = Users.query.get(user_id)
    if not user:
        return jsonify(success=False, message="User not found")

    user.ProfilePath = relative_path
    session['profilepath'] = relative_path
    db.session.commit()

    return jsonify(success=True, image_url=relative_path)


from flask import request, jsonify, session

@bp.route('change_password', methods=['POST'])
def change_password():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'success': False, 'message': 'User not logged in'})

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    user = Users.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    if user.Password != old_password:
        return jsonify({'success': False, 'message': 'Old password is incorrect'})

    # update new password
    user.Password = new_password
    db.session.commit()

    return jsonify({'success': True, 'message': 'Password updated successfully'})
