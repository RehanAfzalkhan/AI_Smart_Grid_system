import pandas as pd
import numpy as np
import requests
from datetime import datetime

# Function to fetch real-time weather data
def fetch_weather(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        return {
            "temperature": response["main"]["temp"],
            "wind_speed": response["wind"]["speed"],
            "weather": response["weather"][0]["description"]
        }
    return None

# Generate synthetic grid data
def generate_synthetic_data():
    time_index = pd.date_range(start=datetime.now(), periods=24, freq="H")
    return pd.DataFrame({
        "timestamp": time_index,
        "load_demand_kwh": np.random.randint(200, 500, len(time_index)),
        "solar_output_kw": np.random.randint(50, 150, len(time_index)),
        "wind_output_kw": np.random.randint(30, 120, len(time_index)),
        "grid_health": np.random.choice(["Good", "Moderate", "Critical"], len(time_index))
    })

# Load optimization recommendation
def optimize_load(demand, solar, wind):
    renewable_supply = solar + wind
    if renewable_supply >= demand:
        return "Grid Stable"
    return "Use Backup or Adjust Load"

if __name__ == "__main__":
    print("Backend ready!")
