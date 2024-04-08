from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired
from utils import load_externals, predict_price_from_input, get_parametral_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Load externals
load_externals()

class PredictForm(FlaskForm):
    district_list, rooms_number_list = get_parametral_data()
    district_choices = [(district, district) for district in district_list]
    num_rooms_choices = [(str(room), str(room)) for room in rooms_number_list]
    district = SelectField('District', choices=district_choices, validators=[DataRequired()])
    num_rooms = SelectField('Number of Rooms', choices=num_rooms_choices, validators=[DataRequired()])
    size_sqm = FloatField('Size (m²)', validators=[DataRequired()])
    submit = SubmitField('Predict')

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    form = PredictForm()
    predicted_price = None
    
    if form.validate_on_submit():
        district = form.district.data
        num_rooms = form.num_rooms.data
        size_sqm = form.size_sqm.data
        
        predicted_price = predict_price_from_input(district, num_rooms, size_sqm)
    

    district_list, rooms_number_list = get_parametral_data()
    
    form.district.choices = [(district, district) for district in district_list]
    form.num_rooms.choices = [(str(room), str(room)) for room in rooms_number_list]
    
    return render_template('predict.html', form=form, predicted_price=predicted_price)


if __name__ == '__main__':  
   app.run(host='0.0.0.0', port=8083)
