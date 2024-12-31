from copy import deepcopy

def register_routes(root_api, root="/api"):
    from .controller import api as summary_api

    root_api.add_namespace(deepcopy(summary_api), path=f"{root}/summary")
    return root_api
