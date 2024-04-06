# server/utils.py
import pandas as pd
from joblib import load
from pathlib import Path  # Importing pathlib


# Path for externals
current_directory = Path(__file__)
district_data_path = current_directory.parent / 'district-data.csv'
model_path = current_directory.parent / 'flatprice-predictor.joblib'

# Load externals

__district_data = None
__model = None

def load_externals():
    global __district_data
    global __model
    __district_data = pd.read_csv(district_data_path)
    __model = load(model_path)

def predict_price_from_input(district: str, num_rooms: float, size_sqm: float):
    global __model
    global __district_data

    district = district.lower().strip()

    district_df = pd.DataFrame(columns=__district_data.columns)
    district_df.loc[0] = 0  
    if district in __district_data.columns:
        district_df[district] = 1  
    if 'Unnamed: 0' in district_df.columns:
        district_df.drop('Unnamed: 0', axis=1, inplace=True)

    # Make prediction
    input_data = pd.DataFrame({
        'Number of rooms': [num_rooms],
        'Size (m²)': [size_sqm]
    })
    input_data = pd.concat([input_data, district_df], axis=1)
    predicted_price = __model.predict(input_data)

    return round(predicted_price[0], 2)


def get_parametral_data():
    global __district_data

    district_df = __district_data.copy()
    district_list = district_df.columns.tolist()[1:]
    rooms_number_list = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]
    return district_list, rooms_number_list

    


if __name__ == '__main__':
   load_externals()  
   get_parametral_data()

