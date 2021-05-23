from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

from util import get_data, get_page_by_code, get_page_by_title

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# * Routes
class mainApi(Resource):
    def get(self):
        code = request.args.get('code')
        title = request.args.get('title')
        if code is None and title is None:
            return {"error": "invalid params"}, 400
        elif code is None:
            if len(title) <= 2:
                return {"error": "param too short"}, 400
            else:
                soup = get_page_by_title(title)
                jsonData = get_data(soup)
                return jsonData, 200 
        else:
            if len(code) <= 1:
                return {"error": "param too short"}, 400
            else:
                soup = get_page_by_code(code)
                jsonData = get_data(soup)
                return jsonData, 200 

class adminApi(Resource):
    def get(self):
        get_type = request.args.get('type')
        if get_type == "all":
            soup = get_page_by_title("")
            jsonData = get_data(soup)
            return jsonData, 200


# api.add_resource(adminApi, "/aaron")
api.add_resource(mainApi, "/")


if __name__ == "__main__":
    app.run(debug=True)

# * Model
