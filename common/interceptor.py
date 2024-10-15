from app import app


@app.after_request
def setupResponseHeaders(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
