from .expenses import register_routes as register_expenses

def register_routes(api):
    register_expenses(api)
