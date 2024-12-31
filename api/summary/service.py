from api.expenses.service import ExpenseService
from api.incomes.service import IncomeService
from api.savings.service import SavingValueService

class SummaryService:
    @staticmethod
    def get_summary(year: int, month: int):
        expenses = ExpenseService.get_expense_list(year=year, month=month)
        savings = SavingValueService.get_unused_by_date(year=year, month=month)
        incomes = IncomeService.get_incomes_list(year=year, month=month)

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
