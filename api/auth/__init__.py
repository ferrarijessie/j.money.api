from copy import deepcopy

def register_routes(root_api, root="/api"):
    from .controller import api as auth_api

    root_api.add_namespace(deepcopy(auth_api), path=f"{root}/auth")
    return root_api