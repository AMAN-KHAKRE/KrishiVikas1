from flask import Flask, request, jsonify
import pickle
import requests
from flask_cors import CORS

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Load the model and encoders
try:
    with open('kaggle_crop_model.pkl', 'rb') as file:
        data = pickle.load(file)
        model = data['model']
        crop_encoder = data['crop_encoder']
        label_encoders = data.get('label_encoders', {})
except Exception as e:
    print(f"Error loading model: {e}")
    raise e

# Weather API Configuration
API_KEY = "1986453606a47823a947378873e2ed58"  # Replace with your actual API key

def get_weather_data(city):
    """Fetch current weather data for the specified city using the Weatherstack API."""
    url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            if 'current' in weather_data:
                weather_info = weather_data['current']
                return {
                    'temperature': weather_info.get('temperature', None),
                    'humidity': weather_info.get('humidity', None),
                    'uv_index': weather_info.get('uv_index', None),
                }
        print(f"Weatherstack API error: {response.json()}")
        return {'temperature': None, 'humidity': None, 'uv_index': None}
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {'temperature': None, 'humidity': None, 'uv_index': None}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        print("Received input data:", input_data)  # Debug log

        # Required fields
        required_fields = [
            'city', 'nitrogen', 'phosphorus', 'potassium', 'ph_value', 
            'rainfall', 'farm_area', 'irrigation_type', 'fertilizer_used',
            'pesticide_used', 'soil_type', 'season'
        ]

        # Validate input
        missing_fields = [field for field in required_fields if field not in input_data or input_data[field] is None]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400

        # Parse input data
        city = input_data['city']
        nitrogen = float(input_data['nitrogen'])
        phosphorus = float(input_data['phosphorus'])
        potassium = float(input_data['potassium'])
        pH_value = float(input_data['ph_value'])
        rainfall = float(input_data['rainfall'])
        farm_area = float(input_data['farm_area'])
        irrigation_type = input_data['irrigation_type']
        fertilizer_used = int(input_data['fertilizer_used'])
        pesticide_used = int(input_data['pesticide_used'])
        soil_type = input_data['soil_type']
        season = input_data['season']

        # Fetch weather data
        weather_data = get_weather_data(city)
        temperature = weather_data.get('temperature')
        humidity = weather_data.get('humidity')
        uv_index = weather_data.get('uv_index')

        if None in [temperature, humidity, uv_index]:
            return jsonify({'error': 'Unable to fetch weather data for the specified city'}), 500

        # Encode categorical fields
        try:
            soil_type_encoded = label_encoders['Soil_Type'].transform([soil_type])[0]
            irrigation_type_encoded = label_encoders['Irrigation_Type'].transform([irrigation_type])[0]
            season_encoded = label_encoders['Season'].transform([season])[0]
        except KeyError as ke:
            return jsonify({'error': f'Encoder not found for: {ke}'}), 400
        except Exception as e:
            return jsonify({'error': f'Error during encoding: {e}'}), 500

        # Debugging categorical encoders
        print("Soil types available:", label_encoders['Soil_Type'].classes_)
        print("Irrigation types available:", label_encoders['Irrigation_Type'].classes_)
        print("Seasons available:", label_encoders['Season'].classes_)

        # Prepare feature array
        features = [
            farm_area, irrigation_type_encoded, fertilizer_used, pesticide_used,
            soil_type_encoded, season_encoded, rainfall, temperature, humidity, uv_index,
            nitrogen, phosphorus, potassium, pH_value
        ]

        # Predict
        prediction = model.predict([features])
        prediction_proba = model.predict_proba([features])
        recommended_crop = crop_encoder.inverse_transform(prediction)

        return jsonify({
            'recommended_crop': recommended_crop[0],
            'class_probabilities': dict(zip(crop_encoder.classes_, prediction_proba[0]))
        })

    except ValueError as ve:
        return jsonify({'error': f'Invalid data type: {ve}'}), 400
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
