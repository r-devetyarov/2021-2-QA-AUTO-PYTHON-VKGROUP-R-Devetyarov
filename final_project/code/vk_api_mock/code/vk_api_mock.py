#!/usr/bin/env python3.8
import logging.handlers
import os

from flask import Flask, jsonify
import random
app = Flask(__name__)

os.environ['WERKZEUG_RUN_MAIN'] = 'true'
# handler = logging.handlers.RotatingFileHandler(
#     '/tmp/mock_log.txt',
#     maxBytes=1024 * 1024)
# logging.getLogger('werkzeug').setLevel(logging.INFO)
# logging.getLogger('werkzeug').addHandler(handler)
# app.logger.setLevel(logging.INFO)
# app.logger.addHandler(handler)

USERS = {}


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_surname(username):
    if username in USERS:
        return jsonify({"vk_id": USERS[username]}), 200
    else:
        return jsonify(), 404


@app.route("/add_user/<username>", methods=['GET'])
def add_user(username):
    USERS[username] = random.randint(10, 1_000_000_000_000)
    return jsonify({"vk_id": USERS[username]}), 200


if __name__ == "__main__":
    app.run()
