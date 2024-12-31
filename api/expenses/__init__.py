from copy import deepcopy

def register_routes(root_api, root="/api"):
    from .controller import api as expenses_api

    root_api.add_namespace(deepcopy(expenses_api), path=f"{root}/expense")
    return root_api
