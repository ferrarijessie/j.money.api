import pytest

from mock import patch, Mock

from api.incomes.exceptions import (
    IncomeTypeNotFoundException,
    IncomeNotFoundException
)
from api.incomes.service import (
    IncomeTypeService,
    IncomeService
)
from api.incomes.model import (
    Income
)

class TestIncomeTypeService:
    def test_get_all_empty_result(self, client):
        result = IncomeTypeService.get_all()

        assert result == []

    def test_get_all_with_result(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.get_all()

        assert income_type in result

    def test_get_one_non_existent(self, client):
        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.get_one(1)
            
    def test_get_one_with_result(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.get_one(income_type.id)

        assert income_type == result

    def test_create(self, client):
       result = IncomeTypeService.create({
        "name": "New Income Type",
        "recurrent": True
       })

       assert result.id > 0
       assert result.name == "New Income Type"
       assert result.recurrent == True

    def test_update_non_existent(self, client):
        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.update(
                id=1, 
                data={
                    "name": "Edited Income Type",
                    "recurrent": True
                }
            )

    def test_update_success(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.update(
            id=income_type.id, 
            data={
                "name": "Edited Income Type",
                "recurrent": True
            }
        )

        assert result.name == "Edited Income Type"
        assert result.recurrent == True

    def test_delete_non_existen(self, client):
        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.delete(id=1)

    def test_delete_success(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.get_one(income_type.id)
        assert income_type == result

        IncomeTypeService.delete(income_type.id)

        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.get_one(income_type.id)


class TestIncomeService:
    def test_get_all_empty_result(self, client):
        result = IncomeService.get_all()

        assert result == []

    def test_get_all_with_result(self, client, income_factory):
        income = income_factory.create()

        result = IncomeService.get_all()

        assert income in result

    def test_get_one_non_existent(self, client):
        with pytest.raises(IncomeNotFoundException):
            IncomeService.get_one(1)
            
    def test_get_one_with_result(self, client, income_factory):
        income = income_factory.create()

        result = IncomeService.get_one(income.id)

        assert income == result

    def test_create(self, client, income_type_factory):
        income_type = income_type_factory.create()

        data = {
            'value': 100,
            'month': 9,
            'year': 2024,
            'type_id': income_type.id,
            'received': False
        }
        result = IncomeService.create(data)

        assert result.id > 0
        assert result.value == 100
        assert result.month == 9
        assert result.year == 2024
        assert result.type_id == income_type.id
        assert result.received == False

    def test_update_non_existen(self, client):
        data = {
            'value': 123,
            'received': True
        }

        with pytest.raises(IncomeNotFoundException):
            IncomeService.update(id=1, data=data)

    def test_update_success(self, client, income_factory):
        income = income_factory.create()
        data = {
            'value': 123,
            'received': True
        }

        result = IncomeService.update(id=income.id, data=data)

        assert result.value == 123
        assert result.received == True

    def test_delete_non_existen(self, client):
        with pytest.raises(IncomeNotFoundException):
            IncomeService.delete(id=1)

    def test_delete_success(self, client, income_factory):
        income = income_factory.create()

        result = IncomeService.get_one(income.id)
        assert income == result

        IncomeService.delete(income.id)

        with pytest.raises(IncomeNotFoundException):
            IncomeService.get_one(income.id)

    def test_get_incomes_list(self, client, income_factory, income_type_factory):
        income_type_factory.create(**{'name': 'Salary', 'recurrent': True})
        income_factory.create(**{'year': 2024, 'month': 9})

        result = IncomeService.get_incomes_list(year=2024, month=9)

        assert len(result) == 2

