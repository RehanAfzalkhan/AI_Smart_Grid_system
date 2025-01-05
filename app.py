import streamlit as st
import pandas as pd
import plotly.express as px
from app_backend import fetch_weather, generate_synthetic_data, optimize_load

# Constants
API_KEY = "84e26811a314599e940f343b4d5894a7"
LOCATION = "Pakistan"

# Sidebar
st.sidebar.title("Smart Grid Dashboard")
location = st.sidebar.text_input("Enter Location", LOCATION)

# Fetch and display weather data
weather = fetch_weather(API_KEY, location)
if weather:
    st.sidebar.write(f"Temperature: {weather['temperature']} °C")
    st.sidebar.write(f"Wind Speed: {weather['wind_speed']} m/s")
    st.sidebar.write(f"Weather: {weather['weather']}")



# Tabs
tab_home, tab_storage, tab_trading = st.tabs(["Home", "Power Storage", "Electricity Trade Management"])

# Home Tab
with tab_home:
    st.title("Real-Time Smart Grid Dashboard")

    # Generate synthetic data
    data = generate_synthetic_data()

    # Grid Health
    # st.subheader("Grid Health Overview")
    # grid_health_counts = data["grid_health"].value_counts()
    # st.bar_chart(grid_health_counts)

    # Power Consumption, Generation & Storage Graph
    st.subheader("Power Consumption, Generation & Storage")
    fig = px.line(data, x="timestamp", y=["load_demand_kwh", "solar_output_kw", "wind_output_kw"], 
                  title="Power Consumption, Generation & Storage", labels={"value": "Power (MW)"})
    fig.update_traces(line=dict(width=2))
    st.plotly_chart(fig)

    # Grid Health
    st.subheader("Grid Health Overview")
    grid_health_counts = data["grid_health"].value_counts()
    st.bar_chart(grid_health_counts)

    
    # Optimization Recommendations
    current_demand = data["load_demand_kwh"].iloc[-1]
    current_solar = data["solar_output_kw"].iloc[-1]
    current_wind = data["wind_output_kw"].iloc[-1]
    recommendation = optimize_load(current_demand, current_solar, current_wind)

    st.subheader("Recommendations")
    st.write(f"Current Load Demand: {current_demand} MW")
    st.write(f"Solar Output: {current_solar} MW")
    st.write(f"Wind Output: {current_wind} MW")
    st.write(f"Recommendation: {recommendation}")

# Storage Tab
with tab_storage:
    st.title("Energy Storage Overview")

    # Energy Contribution by Resources
    st.subheader("Energy Contribution Percentage by Resources")
    energy_data = {
        "Wind": 5,
        "Solar": 7,
        "Turbine": 10
    }
    energy_df = pd.DataFrame(list(energy_data.items()), columns=["Source", "Energy (MW)"])
    fig = px.pie(energy_df, values="Energy (MW)", names="Source", title="Energy Contribution by Resources")
    st.plotly_chart(fig)

    # Energy Storage Merge
    st.subheader("Total Energy Stored")
    st.write("Energy stored from all sources:")
    energy_stored = sum(energy_data.values())
    st.write(f"Total Energy Stored: {energy_stored} MW")
    st.write("Energy sources merged into total energy storage:")
    st.write(f"Total Energy Stored in Grid: {energy_stored} MW")

# Trading Tab
with tab_trading:
    st.title("Electricity Trade Management")

    # Simulating Electricity Trade (Energy cubes & trading)
    st.subheader("Energy Trade Overview")
    energy_trade = {
        "USA": 50,
        "Germany": 40,
        "India": 30
    }
    trade_df = pd.DataFrame(list(energy_trade.items()), columns=["Country", "Energy (MW)"])
    fig = px.bar(trade_df, x="Country", y="Energy (MW)", title="Energy Trading Overview")
    st.plotly_chart(fig)

    st.write("Energy cubes available for trading:")
    st.write("The system can trade energy with other countries.")
