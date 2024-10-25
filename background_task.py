import requests
import sqlite3
import time
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
API_KEY = '4c3302d92daffb0d97899f6d5cac3800'  # Replace with your actual API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
FETCH_INTERVAL = 300  # in seconds
THRESHOLD_TEMP = 35  # Define a threshold temperature

# Database setup
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
    date TEXT,
    city TEXT,
    temp REAL,
    max_temp REAL,
    min_temp REAL,
    dominant_condition TEXT
)''')
conn.commit()

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching weather data for {city}: {response.status_code}")
        return None

def process_weather_data(data):
    """Process and extract relevant weather data."""
    temp = data['main']['temp']
    max_temp = data['main']['temp_max']
    min_temp = data['main']['temp_min']
    condition = data['weather'][0]['main']  # Main weather condition
    return temp, max_temp, min_temp, condition

def store_weather_data(date, city, temp, max_temp, min_temp, dominant_condition):
    """Store weather data in the SQLite database."""
    cursor.execute('''
    INSERT INTO weather_data (date, city, temp, max_temp, min_temp, dominant_condition)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, city, temp, max_temp, min_temp, dominant_condition))
    conn.commit()

def check_alerts(temp):
    """Check if temperature exceeds the defined threshold."""
    if temp > THRESHOLD_TEMP:
        logging.warning(f"Alert! Temperature exceeds threshold: {temp:.2f}°C")

def fetch_weather_data():
    """Fetch and process weather data for all cities."""
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    for city in CITIES:
        data = get_weather_data(city)
        if data:
            temp, max_temp, min_temp, condition = process_weather_data(data)
            store_weather_data(today_date, city, temp, max_temp, min_temp, condition)
            logging.info(f"Weather data for {city} stored successfully.")
            check_alerts(temp)

def store_yesterdays_data():
    """Store the previous day's weather data if it's the end of the day."""
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    for city in CITIES:
        # Here you would define the logic to fetch or use previously stored data for yesterday
        # For example, you can retrieve today's data and use it as yesterday's data for demonstration.
        # Ideally, you would want to fetch historical data, but we'll simulate it for now.

        # You can also keep it simple for the example and use existing data, or calculate aggregates here if required
        cursor.execute('''
            SELECT AVG(temp), MAX(max_temp), MIN(min_temp), dominant_condition
            FROM weather_data
            WHERE date = ?
            AND city = ?
        ''', (yesterday_date, city))
        yesterday_data = cursor.fetchone()
        if yesterday_data:
            avg_temp, max_temp, min_temp, condition = yesterday_data
            store_weather_data(yesterday_date, city, avg_temp, max_temp, min_temp, condition)
            logging.info(f"Yesterday's weather data for {city} stored successfully.")

def main():
    """Main loop to fetch weather data at regular intervals."""
    while True:
        fetch_weather_data()
        store_yesterdays_data()
        time.sleep(FETCH_INTERVAL)  # Wait for the defined interval before fetching again

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Stopping the weather data fetch.")
    finally:
        conn.close()
