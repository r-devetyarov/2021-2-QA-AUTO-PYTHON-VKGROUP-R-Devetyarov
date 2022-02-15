#!/usr/bin/env python3.8
import os
import random
import signal

from flask import Flask, jsonify

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


class ServerTerminationError(Exception):
    pass


def exit_gracefully(signum, frame):
    raise ServerTerminationError()


# gracefully exit on -2
signal.signal(signal.SIGINT, exit_gracefully)
# gracefully exit on -15
signal.signal(signal.SIGTERM, exit_gracefully)


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
    try:
        app.run(host='0.0.0.0', port=5000)
    except ServerTerminationError:
        pass
