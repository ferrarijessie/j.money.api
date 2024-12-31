from copy import deepcopy

def register_routes(root_api, root="/api"):
    from .controller import api as incomes_api

    root_api.add_namespace(deepcopy(incomes_api), path=f"{root}/income")
    return root_api