import enum
from database import db
from datetime import datetime

class ExpenseCategoryEnum(enum.Enum):
    PERSONAL = 'personal'
    COMPANY = 'company'
    HOUSE = 'house'
    CARD = 'card'
    SALON = 'salon'
    HEALTH = 'health'


class ExpenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.Enum(ExpenseCategoryEnum), nullable=False, default=ExpenseCategoryEnum.PERSONAL.value)
    recurrent = db.Column(db.Boolean, default=False)
    base_value = db.Column(db.Numeric(precision=10, scale=2))
    
    expense_values = db.relationship('Expense', backref='expense_type', cascade="all,delete", lazy=True)

    @property
    def get_category(self):
        return self.category.value


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    month = db.Column(db.Integer, nullable=False, default=datetime.today().month)
    year = db.Column(db.Integer, nullable=False, default=datetime.today().year)
    type_id = db.Column(db.Integer, db.ForeignKey('expense_type.id'), nullable=False)
    paid = db.Column(db.Boolean, default=False)

    @property
    def expense_type_name(self):
        return self.expense_type.name

    @property
    def category(self):
        return self.expense_type.get_category
