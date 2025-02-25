import datetime

from database import db

from .model import *
from .interface import (
    IncomeInterface, 
    IncomeUpdateInterface, 
    IncomeTypeInterface
)
from .exceptions import (
    IncomeNotFoundException, 
    IncomeTypeNotFoundException
)


class IncomeTypeService:
    @staticmethod
    def get_all(user_id: int):
        return IncomeType.query.filter(IncomeType.user_id == user_id).all()

    @staticmethod
    def get_one(id: int, user_id: int):
        income_type = IncomeType.query.filter(
            IncomeType.user_id == user_id,
            IncomeType.id == id
        ).first()
        if not income_type:
            raise IncomeTypeNotFoundException()
        return income_type

    @staticmethod
    def create(data: IncomeTypeInterface):
        obj = IncomeType(**data)
        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def update(id: int, data: IncomeTypeInterface, user_id: int):
        obj = IncomeTypeService.get_one(id, user_id=user_id)
        current_base_value = obj.base_value

        for key, value in data.items():
            setattr(obj, key, value)

        if current_base_value != data.get('base_value', 0):
            today = datetime.today()
            incomes = Income.query.filter(
                Income.type_id == id,
                Income.year >= today.year,
                Income.received != True
               
            ).all()
            for income in incomes:
                if (income.year == today.year and income.month >= today.month) or income.month > today.month:
                    IncomeService.update(income.id, {'value': data['base_value']}, user_id=user_id)


        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int, user_id: int):
        obj = IncomeTypeService.get_one(id, user_id=user_id)
        db.session.delete(obj)
        db.session.commit()

class IncomeService:
    @staticmethod
    def get_all(user_id: int):
        return db.session.query(Income).join(IncomeType).filter(IncomeType.user_id == user_id).all()

    @staticmethod
    def get_incomes_list(year: int, month: int, user_id: int):
        incomes = []

        income_types = IncomeTypeService.get_all(user_id=user_id)

        for income_type in income_types:
            if income_type.recurrent:
                income = IncomeService._get_or_create(income_type, year, month)
            else:
                income = Income.query.filter(
                    Income.type_id == income_type.id, 
                    Income.month == month, 
                    Income.year == year).first()

            if income:
                data = IncomeInterface({
                    "id": income.id,
                    "type_name": income_type.name,
                    "type_id": income_type.id,
                    "value": income.value,
                    "month": month,
                    "year": year,
                    "received": getattr(income, "received", False)
                })
                incomes.append(data)
        
        return incomes

    @staticmethod
    def get_one(id: int, user_id: int):
        income = db.session.query(Income).join(IncomeType).filter(
            IncomeType.user_id == user_id,
            Income.id == id
        ).first()

        if not income:
            raise IncomeNotFoundException()
        return income

    @staticmethod
    def create(data: IncomeInterface):
        obj = Income(**data)
        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def update(id: int, data: IncomeUpdateInterface, user_id: int):
        obj = IncomeService.get_one(id, user_id=user_id)

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int, user_id: int):
        obj = IncomeService.get_one(id, user_id=user_id)
        db.session.delete(obj)
        db.session.commit()

    @staticmethod
    def _get_or_create(type: IncomeType, year: int, month: int):
        income = Income.query.filter(
            Income.type_id == type.id, Income.month == month, Income.year == year
        ).first()

        if not income:
            data = IncomeInterface({
                "type_id": type.id,
                "value": type.base_value or 0,
                "month": month,
                "year": year,
                "received": False,
            })
            income = IncomeService.create(data)
        return income
