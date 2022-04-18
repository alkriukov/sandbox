from flask import request
from waitress import serve

import backend_api
import producer

@app.route('/')
def index():
    return 'Hello'

@app.route('/api/tags/', methods=['GET'])
def showTags():
    return backend_api.apiShowTags()

@app.route('/api/tag/<tagname>/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def changeTags(tagname):
    response_info = 'URL should end with valid tag/<tagname>/'
    request_data = request.get_data().decode('utf-8', errors='ignore')
    if tagname:
        response_info = backend_api.apiChangeTags(request.method, request_data, tagname)
        if request.method != 'GET' and response_info.status == 200:
            pass # producer.publish
    return response_info

@app.route('/api/connection/', methods=['GET', 'PUT', 'DELETE'])
def changeConnections():
    request_data = request.get_data().decode('utf-8', errors='ignore')
    response_info = backend_api.apiChangeConnections(request.method, request_data)
    return response_info

@app.route('/api/votes/', methods=['GET', 'POST'])
def setVotes():
    request_data = request.get_data().decode('utf-8', errors='ignore')
    response_info = backend_api.apiSetVotes(request.method, request_data)
    return response_info

@app.route('/api/vote/<up_or_down>/', methods=['PUT'])
def vote(up_or_down):
    response_info = 'URL should end with vote/up/ or vote/down/'
    request_data = request.get_data().decode('utf-8', errors='ignore')
    if up_or_down and (up_or_down in ['up', 'down']):
        response_info = backend_api.apiVote(request.method, request_data, up_or_down)
    return response_info


if __name__ == "__main__":
    if backend_api.this_is_prod:
        serve(backend_api.app, host='0.0.0.0', port=5000)
    else:        
        backend_api.app.run(debug=True, host='0.0.0.0')


