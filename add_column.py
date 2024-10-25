import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Check if the avg_temp column already exists
cursor.execute("PRAGMA table_info(weather_data);")
columns = [column[1] for column in cursor.fetchall()]

if 'avg_temp' not in columns:
    # Add avg_temp column if it doesn't exist
    cursor.execute("ALTER TABLE weather_data ADD COLUMN avg_temp REAL;")
    print("Column 'avg_temp' added to 'weather_data'.")
else:
    print("Column 'avg_temp' already exists in 'weather_data'.")

# Commit changes and close the connection
conn.commit()
conn.close()
