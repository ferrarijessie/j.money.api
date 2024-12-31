from .expenses import register_routes as register_expenses
from .incomes import register_routes as register_incomes

def register_routes(api):
    register_expenses(api)
    register_incomes(api)
