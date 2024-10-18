from flask import Flask, abort, jsonify, request
from eventlet import wsgi
import eventlet
import config
import records

_app = Flask(__name__)


@_app.post('/push/participant')
def push_participant():
    if request.headers.get('api-key') == config.web_api_key:
        data = request.get_json()
        try:
            records.add_participant_response_entry(
                str(data['email']).lower(), data['discord_username'])
            return jsonify(
                {'email': str(data['email']).lower(), 'discord_username': data['discord_username'].lower()})
        except BaseException:
            abort(400)

    else:
        abort(403)


@_app.post('/push/mentor')
def push_mentor():
    if request.headers.get('api-key') == config.web_api_key:
        data = request.get_json()
        try:
            records.add_mentor_response_entry(
                str(data['email']).lower(), data['discord_username'])
            return jsonify(
                {'email': str(data['email']).lower(), 'discord_username': data['discord_username'].lower()})
        except BaseException:
            abort(400)

    else:
        abort(403)


@_app.post('/push/judge')
def push_judge():
    if request.headers.get('api-key') == config.web_api_key:
        data = request.get_json()
        try:
            records.add_judge_response_entry(
                str(data['email']).lower(), data['discord_username'])
            return jsonify(
                {'email': str(data['email']).lower(), 'discord_username': data['discord_username'].lower()})
        except BaseException:
            abort(400)

    else:
        abort(403)


def start():
    wsgi.server(eventlet.listen(('0.0.0.0', config.web_port)), _app)
