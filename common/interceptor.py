from app import app
from flask import make_response

@app.after_request
def setup_response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

    # response_data = {
    #     'message': 'Task Received!',
    #     'message_code': '',
    #     'data': response.get_json()}
    # if not response.get_json():
    #     response = make_response(response_data, 204)
    # else:
    #     response = make_response(response_data, 200)
