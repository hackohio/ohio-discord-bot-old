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
            records.add_participant_response_entry(data['email'], data['discord_tag'])
            return jsonify({'data': data['email'], 'discord_tag': data['discord_tag']})
        except:
            abort(400)
            
    else:
        abort(403)

def start():
    wsgi.server(eventlet.listen(('0.0.0.0', config.web_port)), _app)
