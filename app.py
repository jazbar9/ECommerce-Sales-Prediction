from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from model import predict_sales
from dotenv import load_dotenv
import os

load_dotenv()

# APP FLASK

app = Flask(__name__)


##CONFIGURACION DE SQLALCHEMY ####
#app.app_context().push 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



## CREAMOS UNA CLASE QUE VA A CONVERTIRSE EN UNA TABLA SQL
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    quantity_sold = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day_of_week = db.Column(db.Integer)
    order_hour = db.Column(db.Integer)
    is_weekend = db.Column(db.Integer)
    prediction_gbp = db.Column(db.Float)
    
## CREAMOS UN ESQUEMA PAARA SERIALIZAR LOS DATOS
ma = Marshmallow(app)
class SaleSchema(ma.Schema):
    id = ma.Integer()
    country = ma.Str()
    quantity_sold = ma.Int()
    month = ma.Int()
    day_of_week = ma.Int()
    order_hour = ma.Int()
    is_weekend = ma.Int()
    prediction_gbp = ma.Float()


## REGISTRAMOS LA TABLA EN LA BASE DE DATOS
#application context para asegurar que Flask tenga acceso a la configuración 
#de la base de datos al momento de crear las tablas

with app.app_context():
    db.create_all()
print('Tablas en base de datos creadas')



# ENDPOINT API


#--------Ruta Principal
@app.route('/')
def index():
    return render_template('index.html')

#--Rutas para Ecommerce API 
###-----POST
@app.route('/sales', methods=['POST'])
def set_data():

    data = request.json

    country = data.get('country')
    quantity_sold = data.get('quantity_sold')
    month = data.get('month')
    day_of_week = data.get('day_of_week')
    order_hour = data.get('order_hour')
    is_weekend = data.get('is_weekend')

    # Diccionario 
    new_features = {
        'country_input': country,
        'quantity_sold': quantity_sold,
        'month': month,
        'day_of_week': day_of_week,
        'order_hour': order_hour,
        'is_weekend': is_weekend
    }

    # Predicción
    prediction = predict_sales(**new_features)

    # GUARDAR EN DB 
    new_sale = Sale(
        country=country,
        quantity_sold=quantity_sold,
        month=month,
        day_of_week=day_of_week,
        order_hour=order_hour,
        is_weekend=is_weekend,
        #prediction_gbp=prediction
        prediction_gbp=round(prediction, 2)
    )

    db.session.add(new_sale)
    db.session.commit()

    # Serializar respuesta
    schema = SaleSchema()
    return jsonify(schema.dump(new_sale))



##---------GET
@app.route('/sales', methods=['GET'])
def get_sales():

    sales = Sale.query.all()
    schema = SaleSchema(many=True)

    return jsonify(schema.dump(sales))


#---GET ID

@app.route('/sales/<int:id>', methods=['GET'])
def get_sale(id):

    sale = Sale.query.get(id)

    if not sale:
        return jsonify({"message": "No encontrado"}), 404

    schema = SaleSchema()
    return jsonify(schema.dump(sale))

#----PUT

@app.route('/sales/<int:id>', methods=['PUT'])
def update_sale(id):

    sale = Sale.query.get(id)

    if not sale:
        return jsonify({
            "message": "No encontrado"
            }), 404

    data = request.json

    sale.country = data.get('country')
    sale.quantity_sold = data.get('quantity_sold')
    sale.month = data.get('month')
    sale.day_of_week = data.get('day_of_week')
    sale.order_hour = data.get('order_hour')
    sale.is_weekend = data.get('is_weekend')

    # recalcular predicción
    sale.prediction_gbp = predict_sales(
        sale.country,
        sale.quantity_sold,
        sale.month,
        sale.day_of_week,
        sale.order_hour,
        sale.is_weekend
    )

    db.session.commit()

    schema = SaleSchema()
    return jsonify(schema.dump(sale))

#------DELETE
@app.route('/sales/<int:id>', methods=['DELETE'])
def delete_sale(id):

    sale = Sale.query.get(id)

    if not sale:
        return jsonify({"message": "No encontrado"}), 404

    db.session.delete(sale)
    db.session.commit()

    return jsonify({"message": "Eliminado correctamente"})


# RUN SERVER

if __name__ == '__main__':
    app.run(debug=True)
    
