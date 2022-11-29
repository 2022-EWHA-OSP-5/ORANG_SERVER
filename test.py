from flask import Flask, request, jsonify, session, abort, flash
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import *
import sqlite3, os

app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
db.app = app
with app.app_context():
    db.create_all()


#리스트 화면 (필터링 - 카테고리)
@api.route('/restaurant')
class restaurant_list(Resource):
    def get(self):
        data = request.get_json()
        if data['category'] == "all":
            restaurants = Restaurant.query.all()
        else:
            restaurants = Restaurant.query.filter(Restaurant.category == data['category']).all()
        return_data = {
                'message': '식당 리스트 조회 성공',
                'data': [restaurant.serialize() for restaurant in restaurants]
            }
        return return_data

#맛집 세부 화면 - 정보
@api.route('/restaurant/<int:primary_key>/')
class detail_page(Resource):
    def get(self, primary_key):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute('SELECT name FROM restaurants')
        return jsonify(cur.fetchall())

#맛집 세부 화면 - 메뉴
@api.route('/restaurant/<int:pk>/menu_detail')
class detail_menu(Resource):
    def get(self, pk):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute('SELECT * FROM menus')
        return jsonify(cur.fetchmany(size=3))

#맛집 세부 화면 - 메뉴 - 전체 메뉴 보기
@api.route('/restaurant/<int:primary_key>/menu_detail/all')
class detail_menu(Resource):
    def get(self, primary_key):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute('SELECT * FROM menus')
        return jsonify(cur.fetchall())

#맛집 세부 화면 - 리뷰
@api.route('/restaurant/<int:primary_key>/review_detail')
class detail_review(Resource):
    def get(self, primary_key):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute('SELECT * FROM reviews')
        return jsonify(cur.fetchmany(size=2))

#맛집 세부 화면 - 리뷰 - 전체 리뷰 보기
@api.route('/restaurant/<int:primary_key>/review_detail/all')
class detail_review(Resource):
    def get(self, primary_key):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute('SELECT * FROM reviews')
        return jsonify(cur.fetchall())

#북마크 추가
@api.route('/restaurant/<int:primary_key>/bookmark')
class bookmark(Resource):
    def post(self, primary_key):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute('INSERT INTO bookmarks (id, restauarnt_id, user_id) VALUES (?,?,?)', )
        conn.commit()
        flash("북마크에 추가되었습니다!")
    
   
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)