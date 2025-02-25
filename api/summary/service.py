from typing import List

from api.expenses.service import ExpenseService
from api.incomes.service import IncomeService
from api.savings.service import SavingValueService

from .interface import SummaryItem, SummaryItemModelEnum

class SummaryService:
    @staticmethod
    def get_summary(year: int, month: int, user_id: int):
        expenses = ExpenseService.get_expense_list(year=year, month=month, user_id=user_id)
        savings = SavingValueService.get_unused_by_date(year=year, month=month, user_id=user_id)
        incomes = IncomeService.get_incomes_list(year=year, month=month, user_id=user_id)

        expenses_total = sum(expense['value'] for expense in expenses)
        savings_total = sum(saving.value for saving in savings)
        incomes_total = sum(income['value'] for income in incomes)
        balance = incomes_total - (expenses_total + savings_total)

        data = {
            'expenses_total': expenses_total + savings_total,
            'incomes_total': incomes_total,
            'balance': balance
        }
        return data

    @staticmethod
    def get_summary_list(year: int, month: int, user_id: int) -> List[SummaryItem]:
        result = []

        expenses = ExpenseService.get_expense_list(year=year, month=month, user_id=user_id)
        savings = SavingValueService.get_all_by_date(year=year, month=month, user_id=user_id)
        incomes = IncomeService.get_incomes_list(year=year, month=month, user_id=user_id)

        for expense in expenses:
            result.append(SummaryItem(
                id=expense['id'],
                value=expense['value'],
                type_name=expense['type_name'],
                type_id=expense['type_id'],
                month=expense['month'],
                year=expense['year'],
                status=expense['paid'],
                model=SummaryItemModelEnum.EXPENSE.value
            ))
        
        for income in incomes:
            result.append(SummaryItem(
                id=income['id'],
                value=income['value'],
                type_name=income['type_name'],
                type_id=income['type_id'],
                month=income['month'],
                year=income['year'],
                status=income['received'],
                model=SummaryItemModelEnum.INCOME.value
            ))

        for saving in savings:
            result.append(SummaryItem(
                id=saving.id,
                value=saving.value,
                type_name=saving.type_name,
                type_id=saving.type_id,
                month=saving.month,
                year=saving.year,
                status=saving.used,
                model=SummaryItemModelEnum.SAVING.value
            ))

        return result