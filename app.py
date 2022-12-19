"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

toolbar = DebugToolbarExtension(app)



connect_db(app)



@app.route('/')
def index_page():
    """render home page"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes = cupcakes)

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
    # can call response.data.cupcake in JQuery since we jsonify cupcake below
    response_json = jsonify(cupcake = new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods = ["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.id = id
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods = ["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = "Deleted")

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # flavor = db.Column(db.Text, nullable=False)
    # size = db.Column(db.Text, nullable=False)
    # rating = db.Column(db.Float, nullable=False)
    # image = db.Column(db.String(300), default = DEFAULT_IMAGE_URL, nullable = False)



# Further Study
# Add tests to make sure that the GET/PATCH/DELETE routes return a 404 when the cupcake cannot be found.

# Add functionality for searching for cupcakes where you can type in a search term, submit to the backend and see a newly filtered list of cupcakes.

# HINT: Make sure a search term is passed to the backend and that you are using a LIKE or ILIKE SQL query to search.

# Refactor your front-end code to be object-oriented using class methods to fetchAllCupcakes and createCupcakes and instance methods for updating and deleting cupcakes as well as searching for cupcakes.

# Refactor your HTML page to render a form created by WTForms.

# Enhance your search functionality so that you do not need to wait to submit to filter by flavors.

# Add functionality on the front-end to update a cupcake.

# Are you still here?? Then add another table for ingredients. When you add or edit a cupcake, you can identify what ingredients you need for that cupcake. You should also have a page where you can add or edit ingredients.