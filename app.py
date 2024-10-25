from flask import Flask, jsonify, render_template
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_daily_weather_summary():
    """Retrieve daily weather summaries from the database."""
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Get today's date and yesterday's date
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    cursor.execute('''
    SELECT city, AVG(temp) as avg_temp, MAX(max_temp) as max_temp, MIN(min_temp) as min_temp,
           dominant_condition
    FROM weather_data
    WHERE date IN (?, ?)
    GROUP BY city
    ''', (yesterday, today))

    summary = cursor.fetchall()
    conn.close()

    return summary

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/weather-summary')
def weather_summary():
    """API endpoint to get the daily weather summary."""
    summary = get_daily_weather_summary()
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
