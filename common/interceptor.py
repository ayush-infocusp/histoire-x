from app import app


@app.after_request
def setup_response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
