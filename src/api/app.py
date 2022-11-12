from flask import Flask
from flask_cors import CORS
from waitress import serve  # do not remove

from src.api.routes import api

def create_app():
    app = Flask(__name__)
    CORS(app, support_credentials=True)
    app.register_blueprint(api)
    return app


if __name__ == "__main__":
    app = create_app()
    serve(app, host='0.0.0.0', port=8000, url_scheme='https')
    # app.run(debug=True, port=8000, host='0.0.0.0')
    # app.run(debug=False, port=8000, host='0.0.0.0',  ssl_context=('./ml-api.mystry.world/fullchain1.pem', './ml-api.mystry.world/privkey1.pem'))

