#!/usr/bin/env python3.8

import json
import os
from uuid import uuid4

import requests
from flask import Flask, request, jsonify
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

users_data = {}

external_host = os.environ['EXTERNAL_HOST']
external_port = os.environ['EXTERNAL_PORT']
base_url = f"http://{external_host}:{external_port}"


@app.route("/create_user", methods=["POST"])
def create_user():
    user_name = json.loads(request.data)['name']
    if user_name not in users_data:
        user_id = uuid4()
        users_data[user_name] = {}
        users_data[user_name]["id"] = user_id
        return jsonify({'user_id': users_data[user_name]}), 201

    else:
        return jsonify(f'User_name {user_name} already exists: id: {users_data[user_name]}'), 400


@app.route('/get_user/<user_name>', methods=['GET'])
def get_user_id_via_name(user_name):
    if user_name in users_data:
        return jsonify(f"{users_data[user_name]}"), 200
    else:
        return jsonify(f"User with id {user_name} not found"), 404


@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        response = requests.delete(f"{base_url}/delete_user/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f'Unable to delete user from external system 1:\n{e}')


@app.route('/change_user', methods=['PUT'])
def change_user():
    new_user_data = json.loads(request.data)
    try:
        response = requests.put(f"{base_url}/change_user", json=new_user_data)
        print(response.text)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f'Unable to delete user from external system 1:\n{e}')


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '5000')
    WSGIRequestHandler.protocol_version = "HTTP/1.1"

    app.run(host, port)
