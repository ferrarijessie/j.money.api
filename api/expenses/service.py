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
    def get_all(user_id: int):
        return ExpenseType.query.filter(ExpenseType.user_id == user_id).all()

    @staticmethod
    def get_one(id: int, user_id: int):
        expense_type = ExpenseType.query.filter(
            ExpenseType.id == id, ExpenseType.user_id == user_id).first()

        if not expense_type:
            raise ExpenseTypeNotFoundException
        return expense_type

    @staticmethod
    def get_by_category(category: str, user_id: int):
        return ExpenseType.query.filter(
            ExpenseType.category == category, 
            ExpenseType.user_id == user_id
        ).all()

    @staticmethod
    def create(data: ExpenseTypeInterface):
        obj = ExpenseType(**data)
        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def update(id: int, data: ExpenseTypeInterface, user_id: int):
        obj = ExpenseTypeService.get_one(id, user_id=user_id)
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
                    ExpenseService.update(expense.id, {'value': data['base_value']}, user_id=user_id)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int, user_id: int):
        obj = ExpenseTypeService.get_one(id, user_id=user_id)

        db.session.delete(obj)
        db.session.commit()


class ExpenseService:
    @staticmethod
    def get_all(user_id: int):
        return db.session.query(Expense).join(ExpenseType).filter(ExpenseType.user_id == user_id).all()

    @staticmethod
    def get_one(id: int, user_id: int):
        expense = db.session.query(Expense).join(ExpenseType).filter(
            ExpenseType.user_id == user_id,
            Expense.id == id
        ).first()
        if not expense:
            raise ExpenseNotFoundException()
        return expense
 
    @staticmethod
    def get_by_category(category: str, user_id: int):
        types = ExpenseTypeService.get_by_category(category=category, user_id=user_id)
        type_ids = [t.id for t in types]
        return Expense.query.filter(Expense.type_id.in_(type_ids)).all()

    @staticmethod
    def create(data: ExpenseInterface):
        obj = Expense(**data)
        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def update(id: int, data: ExpenseUpdateInterface, user_id: int):
        obj = ExpenseService.get_one(id, user_id=user_id)

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int, user_id: int):
        obj = ExpenseService.get_one(id, user_id=user_id)
        db.session.delete(obj)
        db.session.commit()

    @staticmethod
    def get_expense_list(month: int, year: int, user_id: int, category: str = 'all'):
        expenses = []

        if category != 'all':
            expense_types = ExpenseTypeService.get_by_category(category=category, user_id=user_id)
        else:
            expense_types = ExpenseTypeService.get_all(user_id=user_id)

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
                    "type_name": expense_type.name,
                    "type_id": expense_type.id,
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
