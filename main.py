from flask import Flask, jsonify, request, make_response
import endpoints_controller
from db import create_tables

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response

@app.route('/api/', methods=["GET"])
def get_all_endpoints():
    endpoints = endpoints_controller.get_all_endpoints()
    return jsonify(endpoints)

@app.route('/api/details/<id>', methods=["GET"])
def get_endpoint_details(id):
    endpoint = endpoints_controller.get_by_id(id)
    if(endpoint == -1):
        return make_response(jsonify(endpoint), 404)
    return jsonify(endpoint)

@app.route('/api/generate/', methods=["GET"])
def generate():
    endpoint = endpoints_controller.generate_endpoint()
    return jsonify(endpoint)

@app.route('/<id>', methods=["GET", "POST"])
def endpointHit(id):
    result = endpoints_controller.store_succesfull_hit(id,  request)
    
    return ("<h1>" + str(result) + "</h1>")

@app.route('/api/delete/<id>', methods=["GET"])
def end_api(id):
    result = endpoints_controller.end_api(id)
    
    return jsonify(result)

if __name__ == "__main__":
    create_tables()
    app.run('0.0.0.0', port = 8000)