import pytest

from api.savings.service import (
    SavingTypeService,
    SavingValueService
)
from api.savings.model import (
    SavingType,
    SavingValue
)
from api.savings.exceptions import (
    SavingTypeNotFoundException,
    SavingValueNotFoundException
)


class TestSavingTypeService:
    def test_get_all_empty_result(self, client):
        result = SavingTypeService.get_all()

        assert result == []

    def test_get_all_with_result(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()

        result = SavingTypeService.get_all()

        assert saving_type in result

    def test_get_active_empty_result(self, client, saving_type_factory):
        saving_type_factory.create(active=False)

        result = SavingTypeService.get_active()

        assert len(result) == 0

    def test_get_active_with_result(self, client, saving_type_factory):
        active_saving_type = saving_type_factory.create()
        inactive_saving_type = saving_type_factory.create(active=False)

        result = SavingTypeService.get_active()

        assert active_saving_type in result
        assert inactive_saving_type not in result
    
    def test_get_one_non_existent(self, client):
        with pytest.raises(SavingTypeNotFoundException):
            SavingTypeService.get_one(1)

    def test_get_one_with_result(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()

        result = SavingTypeService.get_one(saving_type.id)

        assert saving_type == result

    def test_create(self, client):
        result = SavingTypeService.create({
            'name': 'New Saving Type'
        })

        assert isinstance(result, SavingType)
    
    def test_update_non_existent(self, client):
        with pytest.raises(SavingTypeNotFoundException):
            SavingTypeService.update(1, {'name': 'Edited Saving Type'})

    def test_update_success(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()

        result = SavingTypeService.update(saving_type.id, {'name': 'Edited Saving Type'})

        assert result.name == 'Edited Saving Type'
    
    def test_delete_non_existent(self, client):
        with pytest.raises(SavingTypeNotFoundException):
            SavingTypeService.delete(1)

    def test_delete_success(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()
        
        result = SavingTypeService.get_one(saving_type.id)
        assert result == saving_type

        SavingTypeService.delete(saving_type.id)

        with pytest.raises(SavingTypeNotFoundException):
            SavingTypeService.get_one(saving_type.id)


class TestSavingValueService:
    def test_get_all_empty_result(self, client):
        result = SavingValueService.get_all()

        assert result == []

    def test_get_all_with_result(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()

        result = SavingValueService.get_all()

        assert saving_value in result
    
    def test_get_one_non_existent(self, client):
        with pytest.raises(SavingValueNotFoundException):
            SavingValueService.get_one(1)

    def test_get_one_with_result(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()

        result = SavingValueService.get_one(saving_value.id)

        assert saving_value == result

    def test_create(self, client, saving_type_factory):
        saving_type = saving_type_factory.create()
        data = {
            'value': 100,
            'month': 9,
            'year': 2024,
            'type_id': saving_type.id,
            'used': False
        }

        result = SavingValueService.create(data)

        assert isinstance(result, SavingValue)
    
    def test_update_non_existent(self, client):
        data = {
            'value': 500,
            'used': True
        }

        with pytest.raises(SavingValueNotFoundException):
            SavingValueService.update(1, data)

    def test_update_success(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()
        data = {
            'value': 500,
            'used': True
        }

        result = SavingValueService.update(saving_value.id, data)

        assert result.value == 500
        assert result.used == True
    
    def test_delete_non_existent(self, client):
        with pytest.raises(SavingValueNotFoundException):
            SavingValueService.delete(1)

    def test_delete_success(self, client, saving_value_factory):
        saving_value = saving_value_factory.create()
        
        result = SavingValueService.get_one(saving_value.id)
        assert result == saving_value

        SavingValueService.delete(saving_value.id)

        with pytest.raises(SavingValueNotFoundException):
            SavingValueService.get_one(saving_value.id)

    def test__get_unused_by_type_and_date(self, client, saving_type_factory, saving_value_factory):
        saving_type = saving_type_factory.create()
        used_saving_value = saving_value_factory.create(
            value=100, used=True, type_id=saving_type.id, year=2024, month=9
        )    
        used_saving_value_different_month = saving_value_factory.create(
            value=100, used=True, type_id=saving_type.id, year=2024, month=10
        )  
        unused_saving_value = saving_value_factory.create(
            value=200, used=False, type_id=saving_type.id, year=2024, month=9
        )    
          
        unused_saving_value_different_month = saving_value_factory.create(
            value=200, used=False, type_id=saving_type.id, year=2024, month=10
        )     

        result = SavingValueService._get_unused_by_type_and_date(type_id=saving_type.id, year=2024, month=10)

        assert used_saving_value not in result
        assert unused_saving_value in result
        assert unused_saving_value_different_month not in result
        assert used_saving_value_different_month not in result

    def test__get_used_by_type_and_date(self, client, saving_type_factory, saving_value_factory):
        saving_type = saving_type_factory.create()
        used_saving_value = saving_value_factory.create(
            value=100, used=True, type_id=saving_type.id, year=2024, month=9
        )    
        used_saving_value_different_month = saving_value_factory.create(
            value=100, used=True, type_id=saving_type.id, year=2024, month=10
        )  
        unused_saving_value = saving_value_factory.create(
            value=200, used=False, type_id=saving_type.id, year=2024, month=9
        )    
          
        unused_saving_value_different_month = saving_value_factory.create(
            value=200, used=False, type_id=saving_type.id, year=2024, month=10
        )     
        result = SavingValueService._get_used_by_type_and_date(type_id=saving_type.id, year=2024, month=10)

        assert unused_saving_value not in result
        assert used_saving_value in result
        assert unused_saving_value_different_month not in result
        assert used_saving_value_different_month in result

    def test__get_balance_by_type_and_date(self, client, saving_type_factory, saving_value_factory):
        saving_type = saving_type_factory.create()
        saving_value_factory.create(value=100, used=True, type_id=saving_type.id, year=2024, month=9)    
        saving_value_factory.create(value=100, used=True, type_id=saving_type.id, year=2024, month=10)  
        saving_value_factory.create(value=200, used=False, type_id=saving_type.id, year=2024, month=9)    
        saving_value_factory.create(value=200, used=False, type_id=saving_type.id, year=2024, month=10)          

        result = SavingValueService._get_balance_by_type_and_date(type_id=saving_type.id, year=2029, month=10)

        assert result == 200

    def test_get_savings_summary_list(self, client, saving_type_factory, saving_value_factory):
        saving_type = saving_type_factory.create()
        saving_value_factory.create(value=100, used=True, type_id=saving_type.id, year=2024, month=9)    
        saving_value_factory.create(value=200, used=False, type_id=saving_type.id, year=2024, month=9)

        result = SavingValueService.get_savings_summary_list(year=2024, month=10)

        assert len(result) == 1
        assert result[0]['saving_type_id'] == saving_type.id
        assert result[0]['name'] == saving_type.name
        assert result[0]['balance'] == 100

    def test_get_unused_by_date(self, client, saving_value_factory):
        saving_value = saving_value_factory.create(year=2024, month=9, used=False)

        result = SavingValueService.get_unused_by_date(year=2024, month=9)

        assert len(result) == 1
        assert saving_value in result
