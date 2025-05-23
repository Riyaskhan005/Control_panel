
from Alimas_app.extensions import db


class CustomerEntry(db.Model):
    __tablename__ = 'customer_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.Text(255), nullable=False)
    today_special = db.Column(db.Text(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.Text(50), nullable=False)
    # created_on = db.Column(DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(20), nullable=False, default="Active")


    def __repr__(self):
        return f'<CustomerEntry>'
class SnackEntry(db.Model):
    __tablename__ = 'Snacks_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    snacks_name = db.Column(db.Text(255), nullable=False)
    today_special = db.Column(db.Text(255), nullable=False)
    snack_price = db.Column(db.Float, nullable=False)
    # created_on = db.Column(DateTime, nullable=False, default=func.now())
    status = db.Column(db.Text(20), nullable=False, default="Active")

    def __repr__(self):
        return f'<SnackEntry>'
    
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    First_name = db.Column(db.Text(255), nullable=False)
    Last_name = db.Column(db.Text(255), nullable=False)
    Email = db.Column(db.Text(255), nullable=False)
    Password = db.Column(db.Text(255), nullable=False)
    # created_on = db.Column(DateTime, nullable=False, default=func.now())
    status = db.Column(db.Text(20), nullable=False, default="Active")

    def __repr__(self):
        return f'<Users>'