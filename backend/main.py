import os

from flask import Flask, request, session

from api.user import user
from api.exam import exam
from api.question import question


def create_flask_app():

    flask_app = Flask(__name__)
    flask_app.secret_key = 'test'


    api_prefix = '/api/v1'
    module_list = [
        user,
        exam,
        question
    ]
    for module in module_list:
        flask_app.register_blueprint(module, url_prefix=api_prefix)

    return flask_app


if __name__ == '__main__':
    create_flask_app().run(debug=True, host='0.0.0.0', port=5000)
