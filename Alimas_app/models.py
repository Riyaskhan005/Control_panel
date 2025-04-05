
from Alimas_app.extensions import db


class CustomerEntry(db.Model):
    __tablename__ = 'customer_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(255), nullable=False)
    today_special = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    # created_on = db.Column(DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(20), nullable=False, default="Active")


    def __repr__(self):
        return f'<CustomerEntry>'
class SnackEntry(db.Model):
    __tablename__ = 'Snacks_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    snacks_name = db.Column(db.String(255), nullable=False)
    today_special = db.Column(db.String(255), nullable=False)
    snack_price = db.Column(db.Float, nullable=False)
    # created_on = db.Column(DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(20), nullable=False, default="Active")

    def __repr__(self):
        return f'<SnackEntry>'