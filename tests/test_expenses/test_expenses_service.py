import pytest

from datetime import datetime

from api.expenses.service import (
    ExpenseTypeService,
    ExpenseService
)
from api.expenses.model import (
    ExpenseType, 
    ExpenseCategoryEnum,
    Expense
)
from api.expenses.exceptions import (
    ExpenseNotFoundException,
    ExpenseTypeNotFoundException,
)


class TestExpenseTypeService:
    def test_get_all_empty_result(self, client):
        result = ExpenseTypeService.get_all()
        
        assert result == []

    def test_get_all_category_with_result(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        result = ExpenseTypeService.get_all()

        assert expense_type in result

    def test_get_one_no_results(self, client):
        id = ExpenseType.query.count() + 1
        with pytest.raises(ExpenseTypeNotFoundException):
            ExpenseTypeService.get_one(id)

    def test_get_one_with_result(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        result = ExpenseTypeService.get_one(expense_type.id)

        assert result == expense_type

    def test_get_by_category_empty_result(self, client):
        result = ExpenseTypeService.get_by_category(ExpenseCategoryEnum.CARD)
        
        assert result == []

    def test_get_by_category_with_result(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        result = ExpenseTypeService.get_by_category(expense_type.category)
       
        assert expense_type in result

    def test_create(self, client):
        result = ExpenseTypeService.create({
            'name': 'Type 1',
            'category': ExpenseCategoryEnum.PERSONAL,
            'recurrent': False
        })

        assert isinstance(result, ExpenseType)
        assert result.name == 'Type 1'
        assert result.category == ExpenseCategoryEnum.PERSONAL
        assert result.recurrent == False

    def test_update_non_existent(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        
        with pytest.raises(ExpenseTypeNotFoundException):
            ExpenseTypeService.update(expense_type.id+1, {'category': ExpenseCategoryEnum.HOUSE})

    def test_update(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        result = ExpenseTypeService.update(expense_type.id, {'category': ExpenseCategoryEnum.HOUSE})
        
        assert result.category == ExpenseCategoryEnum.HOUSE

    def test_delete_non_existent(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()

        with pytest.raises(ExpenseTypeNotFoundException):
            ExpenseTypeService.delete(expense_type.id+1)

    def test_delete(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        id = expense_type.id

        result = ExpenseTypeService.get_one(id)
        assert result == expense_type

        ExpenseTypeService.delete(id)
        
        with pytest.raises(ExpenseTypeNotFoundException):
            ExpenseTypeService.get_one(id)


class TestExpenseService:
    def test_get_all_empty_result(self, client):
        result = ExpenseService.get_all()

        assert result == []

    def test_get_all_with_result(self, client, expense_factory):
        expense = expense_factory.create()
        result = ExpenseService.get_all()

        assert expense in result

    def test_get_one_empty_result(self, client):
        id = Expense.query.count() + 1
        with pytest.raises(ExpenseNotFoundException) as e:
            ExpenseService.get_one(id)

    def test_get_one_with_result(self, client, expense_factory):
        expense = expense_factory.create()
        result = ExpenseService.get_one(expense.id)
        
        assert result == expense

    def test_get_by_category_empty_result(self, client):
        result = ExpenseService.get_by_category(ExpenseCategoryEnum.COMPANY)
        
        assert result == []

    def test_get_by_category_with_result(self, client, expense_factory):
        expense = expense_factory.create()
        result = ExpenseService.get_by_category(expense.expense_type.category)
        
        assert expense in result

    def test_create(self, client, expense_type_factory):
        expense_type = expense_type_factory.create()
        result = ExpenseService.create({
            'value': 100,
            'month': 1,
            'year': 2024,
            'type_id': expense_type.id,
            'paid': False
        })
        
        assert isinstance(result, Expense)
        assert result.value == 100
        assert result.month == 1
        assert result.year == 2024
        assert result.type_id == expense_type.id
        assert result.paid == False

    def test_update_non_existent(self, client, expense_factory):
        expense = expense_factory.create()

        with pytest.raises(ExpenseNotFoundException):
            ExpenseService.update(expense.id+1, {'value': 135, 'paid': True})
        
    def test_update(self, client, expense_factory):
        expense = expense_factory.create()
        result = ExpenseService.update(expense.id, {'value': 135, 'paid': True})
        
        assert result.value == 135
        assert result.paid == True

    def test_delete_non_existent(self, client, expense_factory):
        expense = expense_factory.create()
        id = expense.id + 1
        with pytest.raises(ExpenseNotFoundException) as e:
            ExpenseService.delete(id)

    def test_delete(self, client, expense_factory):
        expense = expense_factory.create()
        id = expense.id

        result = ExpenseService.get_one(id)
        assert result == expense

        ExpenseService.delete(id)

        with pytest.raises(ExpenseNotFoundException) as e:
            ExpenseService.get_one(id)

    def test_get_expense_list(
        self, 
        client, 
        expense_type_factory, 
        expense_factory
    ):
        expense_type_1 = expense_type_factory.create(**{'recurrent': True, 'name': 'Type 1', 'base_value': 100})

        expense_type_2 = expense_type_factory.create(**{'recurrent': True, 'name': 'Type 2'})
        expense_2 = expense_factory.create(**{'type_id': expense_type_2.id, 'month': 9, 'year': 2024, 'paid': True})

        result = ExpenseService.get_expense_list(category=expense_type_1.category.value, month=9, year=2024)
        assert len(result) == 2

        result_1 = [r for r in result if r['type'] == expense_type_1.name][0]
        assert result_1['value'] == expense_type_1.base_value
        assert result_1['month'] == 9
        assert result_1['year'] == 2024
        assert result_1['paid'] == False

        result_2 = [r for r in result if r['type'] == expense_type_2.name][0]
        assert result_2['value'] == expense_2.value
        assert result_2['month'] == expense_2.month
        assert result_2['year'] == expense_2.year
        assert result_2['paid'] == expense_2.paid

    def test_get_expense_list_all_categories(
        self, 
        client, 
        expense_type_factory, 
        expense_factory
    ):
        expense_type_1 = expense_type_factory.create(**{'recurrent': True, 'name': 'Type 1', 'category': ExpenseCategoryEnum.CARD, 'base_value': 100})

        expense_type_2 = expense_type_factory.create(**{'recurrent': True, 'name': 'Type 2', 'category': ExpenseCategoryEnum.HOUSE})
        expense_2 = expense_factory.create(**{'type_id': expense_type_2.id, 'month': 9, 'year': 2024, 'paid': True})

        result = ExpenseService.get_expense_list(month=9, year=2024)
        assert len(result) == 2

        result_1 = [r for r in result if r['type'] == expense_type_1.name][0]
        assert result_1['value'] == expense_type_1.base_value
        assert result_1['month'] == 9
        assert result_1['year'] == 2024
        assert result_1['paid'] == False

        result_2 = [r for r in result if r['type'] == expense_type_2.name][0]
        assert result_2['value'] == expense_2.value
        assert result_2['month'] == expense_2.month
        assert result_2['year'] == expense_2.year
        assert result_2['paid'] == expense_2.paid

    def test__get_or_create_non_existent_no_base_value(self, client, expense_factory):
        expense = expense_factory.create()
        result = ExpenseService._get_or_create(type=expense.expense_type, year=expense.year+1, month=expense.month+1)

        assert isinstance(result, Expense)
        assert result.type_id == expense.type_id
        assert result.month == expense.month+1
        assert result.year == expense.year+1
        assert result.value == 0
        assert result.paid == False

    def test__get_or_create_non_existent_with_base_value(self, client, expense_factory, expense_type_factory):
        expense_type = expense_type_factory.create(recurrent=True, base_value=100)
        expense = expense_factory.create(type_id=expense_type.id)
        result = ExpenseService._get_or_create(type=expense.expense_type, year=expense.year+1, month=expense.month+1)

        assert isinstance(result, Expense)
        assert result.type_id == expense.type_id
        assert result.month == expense.month+1
        assert result.year == expense.year+1
        assert result.value == expense_type.base_value
        assert result.paid == False

    def test__get_or_create_existent(self, client, expense_factory):
        expense = expense_factory.create(**{'paid': True})
        result = ExpenseService._get_or_create(type=expense.expense_type, year=expense.year, month=expense.month)

        assert isinstance(result, Expense)
        assert result.type_id == expense.type_id
        assert result.month == expense.month
        assert result.year == expense.year
        assert result.value == expense.value
        assert result.paid == expense.paid
