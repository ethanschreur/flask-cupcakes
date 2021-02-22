"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy 
from models import Cupcake, connect_db, db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/cupcakes', methods=['GET'])
def cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake(cupcake_id):
    one_cupcake = Cupcake.query.get_or_404(cupcake_id).serialize()
    return jsonify(cupcake = one_cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    new_cupcake = ''
    try:
        new_cupcake = Cupcake(flavor = request.json['flavor'], size = request.json['size'], rating = request.json['rating'], image = request.json['image'])
    except:
        new_cupcake = Cupcake(flavor = request.json['flavor'], size = request.json['size'], rating = request.json['rating'])
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake = new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def edit_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = "Deleted")
