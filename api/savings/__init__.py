from copy import deepcopy

def register_routes(root_api, root="/api"):
    from .controller import api as savings_api

    root_api.add_namespace(deepcopy(savings_api), path=f"{root}/saving")
    return root_api
    