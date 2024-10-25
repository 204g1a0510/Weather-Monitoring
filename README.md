# Weather-Monitoring Dependencies
Python 3.7+
Flask 2.1+
SQLite
Docker (for containerization)
docker-compose (for orchestration)
git clone https://github.com/your-username/weather-monitor.git
cd weather-monitor
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

version: '3'
services:
  flask:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    depends_on:
      - db
  db:
    image: "nouchka/sqlite3"
    container_name: sqlite-db
docker-compose up --build
http://127.0.0.1:5000
curl -X GET http://127.0.0.1:5000/weather
curl -X POST http://127.0.0.1:5000/set_thresholds -H "Content-Type: application/json" -d '{"temperature": 35, "humidity": 70}'
curl -X GET http://127.0.0.1:5000/alerts
python tests.py

