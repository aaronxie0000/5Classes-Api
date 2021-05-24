from util import get_data, get_page_by_code, get_page_by_title
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_marshmallow import Marshmallow
from datetime import date

from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# * Model
class watchListModel(db.Model):
    __tablename__ = "watchlist"
    _id = db.Column("entryid", db.Integer, primary_key=True)
    uid = db.Column("uid", db.String(255))
    name = db.Column('name', db.String(100), nullable=False)
    identifier = db.Column('identifier', db.String(100), nullable=False)
    course_code = db.Column('course_code', db.String(255), nullable=False)
    course_sec = db.Column('course_sec', db.String(100))
    added_on = db.Column('added_on', db.Date())

    def __init__(self, name, identifier, course_code, course_sec=None):
        self.uid = name + identifier
        self.name = name
        self.identifier = identifier
        self.course_code = course_code
        self.course_sec = course_sec
        self.added_on = date.today()


class watchListSchema(ma.Schema):
    class Meta:
        fields = ("name", "identifier", "course_code",
                  "course_sec", "added_on")


watchList_Schema = watchListSchema()
watchList_Schemas = watchListSchema(many=True)


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


class myClassesApi(Resource):
    def get(self):
        name = request.args.get('name')
        id = request.args.get('id')
        if name is None or id is None:
            return {"error": "Need both 'name' and 'id'"}, 400
        # * Get List of Class Codes of name+id from database
        # * Search each class
        # * filter section, if specified (can't serach by section)
        # * get the matches of each class and put into dict of class code and matches
        # * return the total dict


class myProfileApi(Resource):
    def get(self):
        try:
            name = request.args.get("name")
            identifier = request.args.get("identifier")
            this_uid = name + identifier
        except:
            return {"error": "Missing param"}, 400
        raw_data = watchListModel.query.filter(func.lower(watchListModel.uid)==func.lower(this_uid)).all()
        res = watchList_Schemas.dump(raw_data)
        return res

    def put(self):
        json_data = request.get_json()
        data = watchList_Schema.load(json_data)
        try:
            opt_course_sec = str(data["course_sec"])
            if len(opt_course_sec) != 2:
                return {"error": "course section must be two digits (eg. 02)"}
        except:
            opt_course_sec = None
        matches = watchListModel.query.filter_by(name=data["name"], identifier=data["identifier"],
                                   course_code=data['course_code'], course_sec=opt_course_sec).first()
        if matches is not None:
            return {"error": "course already added"}, 400
        try:
            entry = watchListModel(name=data["name"], identifier=data["identifier"],
                                   course_code=data['course_code'], course_sec=opt_course_sec)
            db.session.add(entry)
            db.session.commit()
            res = watchList_Schema.dump(entry)
            return {"added": res}, 201
        except:
            return {"error": "error in params given"}, 400

    def delete(self):
        json_data = request.get_json()
        # Not deserialize as not adding entry to database, just need the dict data
        try:
            this_name = json_data["name"]
            this_identifier = json_data["identifier"]
            this_course_code = json_data["course_code"]
        except:
            return {"error": "Missing param"}, 400

        try:
            match = watchListModel.query.filter_by(
                name=this_name, identifier=this_identifier, course_code=this_course_code).one()
            db.session.delete(match)
            db.session.commit()
            return {"deleted": {"this_name": this_name, "this_identifier": this_identifier, "this_course_code": this_course_code}}
        except:
            return {"error": "Invalid params"}, 400


# api.add_resource(adminApi, "/aaron")
api.add_resource(mainApi, "/")
api.add_resource(myClassesApi, "/mycourses")
api.add_resource(myProfileApi, "/myclasslist")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
