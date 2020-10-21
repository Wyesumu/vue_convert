import requests

from flask import Flask, jsonify, request

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# init SQLAlchemy instance
db = SQLAlchemy(app)

# Db models
class Good(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    quantity = db.Column(db.Integer)
    currency = db.Column(db.String())
    price = db.Column(db.Float)

    def __repr__(self):
        return self.name

    def as_dict():
        list_of_goods = []
        for good in Good.query.all():
            good_as_dict = good.__dict__
            good_as_dict.pop('_sa_instance_state', None)
            list_of_goods.append(good_as_dict)
        return list_of_goods

# create all tables if not exists
db.create_all()

@app.route('/user/cart', methods=['GET', 'POST'])
def goods():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_good = Good(
            name = post_data.get('name'),
            quantity = post_data.get('quantity'),
            currency = post_data.get('currency'),
            price = post_data.get('price'),
        )
        db.session.add(new_good)
        db.session.commit()
        response_object['message'] = 'Good '+ new_good.name +' added!'
    else:
        response_object['goods'] = Good.as_dict()
    return jsonify(response_object)

@app.route('/user/cart/delete_good/<good_id>', methods=['DELETE'])
def delete_good(good_id):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        good = Good.query.get(good_id)
        db.session.delete(good)
        db.session.commit()
        response_object['message'] = 'Good removed!'
    return jsonify(response_object)

@app.route('/user/cart/calculate', methods=['GET', 'POST'])
def calculate_currency():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        goods = post_data.get('goods')
        serialized = serialize_goods(goods)
        response_object['message'] = serialized
    return jsonify(response_object)

def serialize_goods(goods):
    # request exchange rates
    req = requests.get(url = 'https://www.cbr-xml-daily.ru/daily_json.js')
    data = req.json()['Valute']

    usd_rate = data['USD']['Value']
    eur_rate = data['EUR']['Value']

    # using RUB as a universal currency
    rub_summ = 0

    # initially find summary for all goods in RUB
    for good in goods:
        if good['currency'] == 'USD':
            rub_summ += int(good['quantity']) * float(good['price']) * usd_rate
        elif good['currency'] == 'EUR':
            rub_summ += int(good['quantity']) * float(good['price']) * eur_rate
        else:
            rub_summ += int(good['quantity']) * float(good['price'])

    # and then convert RUB summ to other currencies
    usd_summ = rub_summ / usd_rate
    eur_summ = rub_summ / eur_rate

    return {"RUB": rub_summ, "EUR": eur_summ, "USD": usd_summ}


if __name__ == '__main__':
    app.run()
