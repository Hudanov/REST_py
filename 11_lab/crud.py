from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String)
    model = db.Column(db.String)
    price = db.Column(db.Float)
    rating = db.Column(db.Integer)
    displayOption = db.Column(db.Boolean)
    recordingOption = db.Column(db.Boolean)

    def __init__(self, brand="none", model="none",
                 price=0.0, currency="undefined",
                 rating=0, displayOption=False,
                 recordingOption=False):
        self.brand = brand
        self.model = model
        self.price = price
        self.currency = currency
        self.rating = rating 
        self.displayOption = displayOption
        self.recordingOption = recordingOption


class PhoneSchema(ma.Schema):
    class Meta:
        fields = (
            'brand', 'model',
            'price', 'rating',
            'displayOption', 'recordingOption'
        )


phone_schema = PhoneSchema()
phones_schema = PhoneSchema(many=True)
db.create_all()

# endpoint to create new derivative
@app.route("/phone", methods=["POST"])
def add_phone():
    brand = request.json['brand']
    model = request.json['model']
    price = request.json['price']
    rating = request.json['rating']
    displayOption = request.json['displayOption']
    recordingOption = request.json['recordingOption']

    new_phone = Phone(
        brand, model,
        price, rating, displayOption,
        recordingOption
        )

    db.session.add(new_phone)
    db.session.commit()

    return phone_schema.jsonify(new_phone)


# endpoint to show all derivatives
@app.route("/phone", methods=["GET"])
def get_phone():
    all_phones = Phone.query.all()
    result = phones_schema.dump(all_phones)
    return jsonify(result.data)


# endpoint to get derivative detail by id
@app.route("/phone/<id>", methods=["GET"])
def phone_detail(id):
    phone = Phone.query.get(id)
    return phone_schema.jsonify(phone)


# endpoint to update derivative
@app.route("/phone/<id>", methods=["PUT"])
def derivative_update(id):
    phone = Derivative.query.get(id)
    phone.brand = request.json['brand']
    phone.model = request.json['model']
    phone.price = request.json['price']
    phone.rating = request.json['rating']
    phone.displayOption = request.json['displayOption']
    phone.recordingOption = request.json['recordingOption']

    db.session.commit()
    return derivative_schema.jsonify(phone)


# endpoint to delete derivative
@app.route("/phone/<id>", methods=["DELETE"])
def phonee_delete(id):
    phone = Phone.query.get(id)
    db.session.delete(phone)
    db.session.commit()

    return phone_schema.jsonify(phone)


if __name__ == '__main__':
     app.run(debug=True)