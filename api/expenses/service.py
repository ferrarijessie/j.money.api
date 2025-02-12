import datetime

from database import db

from .model import *
from .exceptions import (
    ExpenseNotFoundException, 
    ExpenseTypeNotFoundException,
)
from .interface import (
    ExpenseInterface, 
    ExpenseUpdateInterface, 
    ExpenseReturnInterface,
    ExpenseTypeInterface
)

class ExpenseTypeService:
    @staticmethod
    def get_all():
        return ExpenseType.query.all()

    @staticmethod
    def get_one(id: int):
        expense_type = db.session.get(ExpenseType, id)
        if not expense_type:
            raise ExpenseTypeNotFoundException()
        return expense_type

    @staticmethod
    def get_by_category(category: str):
        return ExpenseType.query.filter(ExpenseType.category == category).all()

    @staticmethod
    def create(data: ExpenseTypeInterface):
        obj = ExpenseType(**data)
        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def update(id: int, data: ExpenseTypeInterface):
        obj = ExpenseTypeService.get_one(id)
        current_base_value = obj.base_value

        for key, value in data.items():
            setattr(obj, key, value)

        if current_base_value != data.get('base_value', 0):
            today = datetime.today()
            expenses = Expense.query.filter(
                Expense.type_id == id,
                Expense.year >= today.year,
                Expense.paid != True
               
            ).all()
            for expense in expenses:
                if (expense.year == today.year and expense.month >= today.month) or expense.month > today.month:
                    ExpenseService.update(expense.id, {'value': data['base_value']})

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int):
        obj = ExpenseTypeService.get_one(id)

        db.session.delete(obj)
        db.session.commit()


class ExpenseService:
    @staticmethod
    def get_all():
        return Expense.query.all()

    @staticmethod
    def get_one(id: int):
        expense = db.session.get(Expense, id)
        if not expense:
            raise ExpenseNotFoundException()
        return expense
 
    @staticmethod
    def get_by_category(category: str):
        types = ExpenseTypeService.get_by_category(category=category)
        type_ids = [t.id for t in types]
        return Expense.query.filter(Expense.type_id.in_(type_ids)).all()

    @staticmethod
    def create(data: ExpenseInterface):
        obj = Expense(**data)
        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def update(id: int, data: ExpenseUpdateInterface):
        obj = ExpenseService.get_one(id)

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int):
        obj = ExpenseService.get_one(id)
        db.session.delete(obj)
        db.session.commit()

    @staticmethod
    def get_expense_list(month: int, year: int, category: str = 'all'):
        expenses = []

        if category != 'all':
            expense_types = ExpenseTypeService.get_by_category(category=category)
        else:
            expense_types = ExpenseTypeService.get_all()

        for expense_type in expense_types:
            if expense_type.recurrent:
                expense = ExpenseService._get_or_create(expense_type, year, month)
            else:
                expense = Expense.query.filter(
                    Expense.type_id == expense_type.id, 
                    Expense.month == month, 
                    Expense.year == year).first()

            if expense:
                data = ExpenseReturnInterface({
                    "id": expense.id,
                    "type": expense_type.name,
                    "value": expense.value,
                    "month": month,
                    "year": year,
                    "paid": getattr(expense, "paid", False),
                    "category": expense_type.category.value
                })
                expenses.append(data)
        
        return expenses

    @staticmethod
    def _get_or_create(type: ExpenseType, year: int, month: int):
        expense = Expense.query.filter(Expense.type_id == type.id, Expense.month == month, Expense.year == year).first()
        if not expense:
            data = ExpenseInterface({
                "type_id": type.id,
                "value": type.base_value or 0,
                "month": month,
                "year": year,
                "paid": False,
            })
            expense = ExpenseService.create(data)
        return expense
