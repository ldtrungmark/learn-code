from flask import Flask
from views import api_v1


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    app.run(debug=True)
