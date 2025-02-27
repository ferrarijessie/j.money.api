from .expenses import register_routes as register_expenses
from .incomes import register_routes as register_incomes
from .savings import register_routes as register_savings
from .summary import register_routes as register_summary
from .auth import register_routes as register_auth

def register_routes(api):
    register_expenses(api)
    register_incomes(api)
    register_savings(api)
    register_summary(api)
    register_auth(api)
