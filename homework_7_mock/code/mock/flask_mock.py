#!/usr/bin/env python3.8
import json
import logging.handlers
import os
import threading

from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

os.environ['WERKZEUG_RUN_MAIN'] = 'true'
handler = logging.handlers.RotatingFileHandler(
    '/tmp/mock_log.txt',
    maxBytes=1024 * 1024)
logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.CRITICAL)
app.logger.addHandler(handler)

SURNAME_DATA = {}
USER_DATA = {}


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify(surname), 200
    else:
        return jsonify(f'Surname for user "{name}" not found'), 404


@app.route("/delete_user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user_id = str(user_id)
    if user_id in USER_DATA:
        USER_DATA.pop(user_id)
        return jsonify(f"Successfully deleted user with id {user_id}"), 200
    else:
        return jsonify(f"User for id {user_id} not found"), 404


@app.route("/change_user", methods=['PUT'])
def change_user_profile():
    error = None
    new_user_data = json.loads(request.data)

    if "id" not in new_user_data:
        error = "Filed 'id' mast have in payload", 400
    elif new_user_data["id"] not in USER_DATA:
        error = f"User with id {new_user_data['id']} not found", 404
    else:
        user_id = new_user_data["id"]

    name = None
    surname = None

    if "name" in new_user_data:
        if isinstance(new_user_data["name"], str):
            name = new_user_data["name"]
        else:
            error = "Filed name must be str", 400

    if "surname" in new_user_data:
        if isinstance(new_user_data["surname"], str):
            surname = new_user_data["surname"]
        else:
            error = "Filed surname must be str", 400

    if error is not None:
        return jsonify(error[0]), error[1]
    else:
        USER_DATA[user_id]["name"] = name if name else USER_DATA[user_id]["name"]
        USER_DATA[user_id]["surname"] = surname if surname else USER_DATA[user_id]["surname"]

        return jsonify(f"Successfully update, new data user:\n"
                       f" name={USER_DATA[user_id]['name']}\n"
                       f" surname={USER_DATA[user_id]['surname']}"), 200


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })

    server.start()
    return server
