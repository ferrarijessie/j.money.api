import pytest

from datetime import datetime

from api.incomes.exceptions import (
    IncomeTypeNotFoundException,
    IncomeNotFoundException
)
from api.incomes.service import (
    IncomeTypeService,
    IncomeService
)

class TestIncomeTypeService:
    def test_get_all_empty_result(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.get_all(user_id=income_type.user_id+1)

        assert result == []

    def test_get_all_with_result(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.get_all(user_id=income_type.user_id)

        assert income_type in result

    def test_get_one_non_existent(self, client, income_type_factory):
        income_type = income_type_factory.create()

        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.get_one(1, user_id=income_type.user_id+1)
            
    def test_get_one_with_result(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.get_one(income_type.id, user_id=income_type.user_id)

        assert income_type == result

    def test_create(self, client, user_factory):
        user = user_factory.create()
        
        result = IncomeTypeService.create({
            "name": "New Income Type",
            "recurrent": True,
            "user_id": user.id
        })
        
        assert result.id > 0
        assert result.name == "New Income Type"
        assert result.recurrent == True

    def test_update_non_existent(self, client, income_type_factory):
        income_type = income_type_factory.create()

        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.update(
                id=income_type.id, 
                data={
                    "name": "Edited Income Type",
                    "recurrent": True
                },
                user_id=income_type.user_id+1
            )

    def test_update_success(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.update(
            id=income_type.id, 
            data={
                "name": "Edited Income Type",
                "recurrent": True
            },
            user_id=income_type.user_id
        )

        assert result.name == "Edited Income Type"
        assert result.recurrent == True
        
    def test_update_will_update_future_values(
        self, 
        client, 
        income_type_factory, 
        income_factory, 
        user_factory
    ):
        user = user_factory.create()
        income_type = income_type_factory.create(
            recurrent=True,
            name='Type 1',
            base_value=100,
            user_id=user.id
        )
        income = income_factory.create(
            type_id=income_type.id, 
            value=income_type.base_value,
            month=datetime.today().month,
            year=datetime.today().year,
            received=False
        )

        result = IncomeTypeService.update(
            income.type_id, 
            {'base_value': 200},
            user_id=user.id
        )

        income = IncomeService.get_one(id=income.id, user_id=user.id)
        
        assert result.base_value == 200
        assert income.value == 200

    def test_delete_non_existen(self, client, income_type_factory):
        income_type = income_type_factory.create()

        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.delete(id=income_type.id, user_id=income_type.user_id+1)

    def test_delete_success(self, client, income_type_factory):
        income_type = income_type_factory.create()

        result = IncomeTypeService.get_one(income_type.id, user_id=income_type.user_id)
        assert income_type == result

        IncomeTypeService.delete(income_type.id, user_id=income_type.user_id)

        with pytest.raises(IncomeTypeNotFoundException):
            IncomeTypeService.get_one(income_type.id, user_id=income_type.user_id)


class TestIncomeService:
    def test_get_all_empty_result(self, client, income_factory):
        income = income_factory.create()

        result = IncomeService.get_all(user_id=income.user_id+1)

        assert result == []

    def test_get_all_with_result(self, client, income_factory):
        income = income_factory.create()

        result = IncomeService.get_all(user_id=income.user_id)

        assert income in result

    def test_get_one_non_existent(self, client, income_factory):
        income = income_factory.create()

        with pytest.raises(IncomeNotFoundException):
            IncomeService.get_one(income.id, user_id=income.user_id+1)
            
    def test_get_one_with_result(self, client, income_factory):
        income = income_factory.create()

        result = IncomeService.get_one(income.id, user_id=income.user_id)

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

    def test_update_non_existen(self, client, income_factory):
        income = income_factory.create()

        data = {
            'value': 123,
            'received': True
        }

        with pytest.raises(IncomeNotFoundException):
            IncomeService.update(id=income.id, data=data, user_id=income.user_id+1)

    def test_update_success(self, client, income_factory):
        income = income_factory.create()
        data = {
            'value': 123,
            'received': True
        }

        result = IncomeService.update(id=income.id, data=data, user_id=income.user_id)

        assert result.value == 123
        assert result.received == True

    def test_delete_non_existen(self, client, income_factory):
        income = income_factory.create()

        with pytest.raises(IncomeNotFoundException):
            IncomeService.delete(id=income.id, user_id=income.user_id+1)

    def test_delete_success(self, client, income_factory):
        income = income_factory.create()

        result = IncomeService.get_one(income.id, user_id=income.user_id)
        assert income == result

        IncomeService.delete(income.id, user_id=income.user_id)

        with pytest.raises(IncomeNotFoundException):
            IncomeService.get_one(income.id, user_id=income.user_id)

    def test_get_incomes_list(self, client, income_factory, income_type_factory, user_factory):
        user = user_factory.create()

        income_type_factory.create(name='Salary', recurrent=True, user_id=user.id)

        income_type_2 = income_type_factory.create(name='Salary', recurrent=True, user_id=user.id)
        income_factory.create(type_id=income_type_2.id, value=100, year=2024, month=9)

        result = IncomeService.get_incomes_list(year=2024, month=9, user_id=user.id)

        assert len(result) == 2

