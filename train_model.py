import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Weather API Configuration
API_KEY = "1986453606a47823a947378873e2ed58"  # Replace with your actual API key

def get_weather_data(city, API_KEY):
    """Fetch current weather data for the specified city using the Weatherstack API."""
    url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            if 'current' in weather_data:
                current_weather = weather_data['current']
                return {
                    'Temperature': current_weather['temperature'],
                    'Humidity': current_weather['humidity'],
                    'UV_Index': current_weather['uv_index']
                }
            else:
                print(f"Error: No weather data found for {city}")
                return {'Temperature': None, 'Humidity': None, 'UV_Index': None}
        else:
            print(f"Error fetching weather data: {response.status_code}, {response.text}")
            return {'Temperature': None, 'Humidity': None, 'UV_Index': None}
    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        return {'Temperature': None, 'Humidity': None, 'UV_Index': None}

# Prompt the user to input the city name
city = input("Enter city name: ")

# Fetch weather data for the input city
weather_data = get_weather_data(city, API_KEY)
if any(v is None for v in weather_data.values()):
    print("Error: Could not fetch complete weather data. Exiting.")
    exit()

print("Fetched Weather Data:", weather_data)

# Load the dataset
data = pd.read_csv("real_time_agriculture_data_with_crops.csv")  # Replace with your dataset filename

# Check distribution of crop types
print("Crop distribution:", data['Crop'].value_counts())

# Add weather data as features to the dataset
data['Temperature(°C)'] = weather_data['Temperature']
data['Humidity(%)'] = weather_data['Humidity']
data['UV_Index'] = weather_data['UV_Index']

# Check for missing values and handle them
if data.isnull().sum().any():
    print("Handling missing values...")
    data = data.dropna()  # You can also use data.fillna() for imputation if needed

# Encode the target variable (Crop) if it is categorical
crop_encoder = LabelEncoder()
data['Crop'] = crop_encoder.fit_transform(data['Crop'])  # Encoding the 'Crop' column

# Define features and target variables
X = data[['Farm_Area(acres)', 'Irrigation_Type', 'Fertilizer_Used(tons)', 'Pesticide_Used(kg)', 
           'Soil_Type', 'Season', 'Rainfall(mm)', 'Temperature(°C)', 'Humidity(%)', 'UV_Index', 
           'Nitrogen', 'Phosphorus', 'Potassium', 'pH_Value']]  # Exclude 'Crop' column from features
y = data['Crop']  # Target (encoded Crop)

# Encode categorical features using LabelEncoder
label_encoders = {}

# Columns to encode
categorical_columns = ['Irrigation_Type', 'Soil_Type', 'Season']

# Encode each categorical column
for column in categorical_columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])  # Modify the column in-place
    label_encoders[column] = le

# Check if the dataset has been transformed correctly
print(X.head())

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the RandomForest model
model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Save the trained model and encoders to a file
with open('kaggle_crop_model.pkl', 'wb') as file:
    pickle.dump({
        'model': model,
        'crop_encoder': crop_encoder,
        'label_encoders': label_encoders
    }, file)

print("Model training complete and saved as 'kaggle_crop_model.pkl'")

# Get input values from the user for prediction
try:
    city = str(input("Enter the name of city: "))
    farm_area = float(input("Enter farm area (acres): "))
    irrigation_type = input("Enter irrigation type: ")
    fertilizer_used = float(input("Enter fertilizer used (tons): "))
    pesticide_used = float(input("Enter pesticide used (kg): "))
    soil_type = input("Enter soil type: ")
    season = input("Enter season: ")
    rainfall = float(input("Enter rainfall (mm): "))
    nitrogen = float(input("Enter nitrogen value: "))
    phosphorus = float(input("Enter phosphorus value: "))
    potassium = float(input("Enter potassium value: "))
    ph_value = float(input("Enter pH value: "))
except ValueError as e:
    print(f"Error: Invalid input. {e}")
    exit()

# Use the weather data to provide additional input features
temperature = weather_data['Temperature']
humidity = weather_data['Humidity']
uv_index = weather_data['UV_Index']

# Encode the categorical features (Irrigation_Type, Soil_Type, Season)
try:
    irrigation_type_encoded = label_encoders['Irrigation_Type'].transform([irrigation_type])[0]
    soil_type_encoded = label_encoders['Soil_Type'].transform([soil_type])[0]
    season_encoded = label_encoders['Season'].transform([season])[0]
except KeyError as e:
    print(f"Error: Invalid categorical input. {e}")
    exit()

# Construct the feature vector for prediction (as a pandas DataFrame)
features_dict = {
    'Farm_Area(acres)': [farm_area],
    'Irrigation_Type': [irrigation_type_encoded],
    'Fertilizer_Used(tons)': [fertilizer_used],
    'Pesticide_Used(kg)': [pesticide_used],
    'Soil_Type': [soil_type_encoded],
    'Season': [season_encoded],
    'Rainfall(mm)': [rainfall],
    'Temperature(°C)': [temperature],
    'Humidity(%)': [humidity],
    'UV_Index': [uv_index],
    'Nitrogen': [nitrogen],
    'Phosphorus': [phosphorus],
    'Potassium': [potassium],
    'pH_Value': [ph_value]
}

# Create a DataFrame with the same columns as during training
features_df = pd.DataFrame(features_dict)

# Ensure the columns are in the same order as during training
features_df = features_df[X.columns]

# Print the input features DataFrame for verification
print("Input features DataFrame for prediction:")
print(features_df)

# Make the prediction using the model
prediction = model.predict(features_df)
print("Raw model prediction:", prediction)

# Decode the predicted crop
recommended_crop = crop_encoder.inverse_transform(prediction)
print("Recommended Crop:", recommended_crop[0])
