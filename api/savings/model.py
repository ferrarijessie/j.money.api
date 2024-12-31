from datetime import datetime

from database import db


class SavingType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, default=False)
    base_value = db.Column(db.Numeric(precision=10, scale=2))

    expense_values = db.relationship('SavingValue', backref='saving_type', lazy=True)


class SavingValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    month = db.Column(db.Integer, nullable=False, default=datetime.today().month)
    year = db.Column(db.Integer, nullable=False, default=datetime.today().year)
    type_id = db.Column(db.Integer, db.ForeignKey('saving_type.id'), nullable=False)
    used = db.Column(db.Boolean, default=False)

    @property
    def type_name(self):
        return self.saving_type.name
