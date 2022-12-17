"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/')
def index_page():
    """render home page"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """return JSON sata on all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def list_cupcake(id):
    """return JSON data on single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods = ["POST"])
def create_cupcake():
    new_cupcake = Cupcake(flavor = request.json["flavor"], size = request.json["size"], 
    rating = request.json["rating"], image = request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake = new_cupcake.serialize())
    return (response_json, 201)



    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # flavor = db.Column(db.Text, nullable=False)
    # size = db.Column(db.Text, nullable=False)
    # rating = db.Column(db.Float, nullable=False)
    # image = db.Column(db.String(300), default = DEFAULT_IMAGE_URL, nullable = False)
