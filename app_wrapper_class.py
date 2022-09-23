from flask import Flask, Response


class EndpointAction(object):
    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response
        

class FlaskAppWrapper(object):
    app = None

    def __init__(self, name, port: int=None):
        self.app = Flask(name)
        self.port = port

        
        self.port = port

    def run(self):
        self.app.run(port=self.port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))
