from database import db

from .model import (
    SavingValue, 
    SavingType
)
from .exceptions import (
    SavingTypeNotFoundException,
    SavingValueNotFoundException
)
from .interface import (
    SavingTypeInterface,
    SavingValueInterface,
    SavingValueUpdateInterface
)


class SavingTypeService:
    @staticmethod
    def get_all():
        return SavingType.query.all()

    @staticmethod
    def get_active():
        return SavingType.query.filter(SavingType.active == True).all()

    @staticmethod
    def get_one(id: int):
        saving_type =  db.session.get(SavingType, id)

        if not saving_type:
            raise SavingTypeNotFoundException()
        return saving_type

    @staticmethod
    def create(data: SavingTypeInterface):
        obj = SavingType(**data)
        db.session.add(obj)
        db.session.commit()

        return obj
    
    @staticmethod
    def update(id: int, data: SavingTypeInterface):
        obj = SavingTypeService.get_one(id)

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int):
        obj = SavingTypeService.get_one(id)

        db.session.delete(obj)
        db.session.commit()


class SavingValueService:
    @staticmethod
    def get_all():
        return SavingValue.query.all()

    @staticmethod
    def get_one(id: int):
        saving_type =  db.session.get(SavingValue, id)

        if not saving_type:
            raise SavingValueNotFoundException()
        return saving_type

    @staticmethod
    def get_savings_summary_list(year: int, month: int):
        savings_summary = []
        saving_types = SavingTypeService.get_active()

        for saving_type in saving_types:
            balance = SavingValueService._get_balance_by_type_and_date(saving_type.id, year, month)
            current_value = 0

            current_month_savings = SavingValue.query.filter(
                SavingValue.type_id == saving_type.id, 
                SavingValue.year == year, 
                SavingValue.month == month,
                SavingValue.used == False
            ).all()
            current_value = sum(saving.value for saving in current_month_savings)

            savings_summary.append({
                'saving_type_id': saving_type.id,
                'name': saving_type.name,
                'balance': balance,
                'current_month_value': current_value
            })

        return savings_summary

    @staticmethod
    def get_all_by_date(year: int, month: int):
        return SavingValue.query.filter(
            SavingValue.year == year,
            SavingValue.month == month
        ).all()

    @staticmethod
    def get_unused_by_date(year: int, month: int):
        return SavingValue.query.filter(
            SavingValue.used == False,
            SavingValue.year == year,
            SavingValue.month == month
        ).all()

    @staticmethod
    def create(data: SavingValueInterface):
        obj = SavingValue(**data)
        db.session.add(obj)
        db.session.commit()

        return obj
    
    @staticmethod
    def update(id: int, data: SavingValueUpdateInterface):
        obj = SavingValueService.get_one(id)

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete(id: int):
        obj = SavingValueService.get_one(id)

        db.session.delete(obj)
        db.session.commit()

    @staticmethod
    def _get_unused_by_type_and_date(type_id: int, year: int, month: int):
        selected_year = SavingValue.query.filter(
            SavingValue.type_id == type_id,
            SavingValue.used == False,
            SavingValue.year == year,
            SavingValue.month < month
        ).all()
        previous_year = SavingValue.query.filter(
            SavingValue.type_id == type_id,
            SavingValue.used == False,
            SavingValue.year < year,
        ).all()
        return selected_year + previous_year

    @staticmethod
    def _get_used_by_type_and_date(type_id: int, year: int, month: int):
        selected_year = SavingValue.query.filter(
            SavingValue.type_id == type_id,
            SavingValue.used == True,
            SavingValue.year == year,
            SavingValue.month <= month
        ).all()
        previous_year = SavingValue.query.filter(
            SavingValue.type_id == type_id,
            SavingValue.used == True,
            SavingValue.year < year,
        ).all()
        return selected_year + previous_year

    @staticmethod
    def _get_balance_by_type_and_date(type_id: int, year: int, month: int):
        used_savings = SavingValueService._get_used_by_type_and_date(type_id, year, month)
        unused_savings = SavingValueService._get_unused_by_type_and_date(type_id, year, month)

        used_value = sum(saving.value for saving in used_savings)
        unused_value = sum(saving.value for saving in unused_savings)

        return unused_value - used_value
