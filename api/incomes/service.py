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
    def get_all():
        return IncomeType.query.all()

    @staticmethod
    def get_one(id: int):
        income_type = db.session.get(IncomeType, id)
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
    def update(id: int, data: IncomeTypeInterface):
        obj = IncomeTypeService.get_one(id)

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int):
        obj = IncomeTypeService.get_one(id)
        db.session.delete(obj)
        db.session.commit()

class IncomeService:
    @staticmethod
    def get_all():
        return Income.query.all()

    @staticmethod
    def get_incomes_list(year: int, month: int):
        incomes = []

        income_types = IncomeTypeService.get_all()

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
                    "type": income_type.name,
                    "value": income.value,
                    "month": month,
                    "year": year,
                    "received": getattr(income, "received", False)
                })
                incomes.append(data)
        
        return incomes

    @staticmethod
    def get_one(id: int):
        income = db.session.get(Income, id)
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
    def update(id: int, data: IncomeUpdateInterface):
        obj = IncomeService.get_one(id)

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int):
        obj = IncomeService.get_one(id)
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
