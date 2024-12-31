from flask import json, Response

def make_json_response(data, code): 
    json_data = json.dumps(data)
    resp = Response(json_data, mimetype='application/json')
    resp.status_code = code

    return resp
