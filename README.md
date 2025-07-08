

# 🌾 KrishiVikash – Smart Crop Prediction System

**KrishiVikash** is a Flask-based web application that predicts the most suitable crop to grow based on real-time weather conditions and soil parameters. 
It leverages machine learning for prediction and integrates a weather API to fetch dynamic environmental data like temperature and humidity.

## 🚀 Features

* 🌦️ Real-time weather data integration using API
* 🌱 Smart crop prediction using trained ML models
* 🧪 Inputs include NPK values, pH, rainfall, and location
* 🌐 Simple and responsive web interface
* 📊 Backend prediction engine using scikit-learn



## 🧠 Technologies Used

* **Frontend**: HTML, CSS, Javascript
* **Backend**: Python, Flask
* **ML Model**: Scikit-learn (Classification)
* **API**: OpenWeatherMap (or any weather API)
* **Deployment**: (Optional) Localhost / Cloud (Render, Heroku, etc.)

---

## 📌 Input Parameters

* **Soil Nutrients**:

  * Nitrogen (N)
  * Phosphorus (P)
  * Potassium (K)
* **Soil pH**
* **Rainfall (mm)**
* **Location (City name)** → for fetching:

  * Temperature (°C)
  * Humidity (%)

---

## 📦 Project Structure

```
krishivikash/
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── model/
│   └── crop_model.pkl
├── app.py
├── weather.py
├── requirements.txt
└── README.md
```



## 🧪 Model Details

* **Type**: Classification model
* **Algorithm**: Random Forest / XGBoost / Decision Tree
* **Dataset**: Public crop recommendation datasets (e.g., from Kaggle)
* **Target**: Crop Label (Rice, Maize, Cotton, etc.)
* **Accuracy**: \~90% depending on dataset and model

---

## ▶️ How to Run the App

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AMAN-KHAKRE/KrishiVikas1.git
   cd krishivikash
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your weather API key**
   In `weather.py`, replace `YOUR_API_KEY` with your actual API key from OpenWeatherMap or similar.

4. **Run the Flask app:**

   ```bash
   python app.py
   ```

5. **Open in Browser:**
   Go to `http://127.0.0.1:5000`

---

## 🔑 Example Weather API Call (OpenWeatherMap)

```http
https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid=YOUR_API_KEY&units=metric
```

Extracts temperature and humidity from the JSON response and passes to the model.

---

## 💻 Sample Prediction Flow

1. User enters soil values + city name
2. App fetches current temperature & humidity using API
3. Model processes combined input and predicts best crop
4. Result displayed on the page

## 🙌 Acknowledgements

* [Kaggle Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
* [OpenWeatherMap API](https://openweathermap.org/api)
* Scikit-learn, Flask Documentation


