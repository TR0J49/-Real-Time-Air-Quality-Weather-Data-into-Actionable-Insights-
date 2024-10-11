import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import requests
import datetime
import random

# Initialize Dash app
app = dash.Dash(__name__)

# API Key and URL
API_KEY = '1d8e5e9b5d3609b70bbb6de6efb15f17'
BASE_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'

# Function to fetch air quality and weather data
def get_air_quality_and_weather(city):
    try:
        # Fetch city weather data (for temperature and humidity)
        city_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        city_data = requests.get(city_url).json()

        if city_data.get('cod') != 200:
            print(f"Error: {city_data.get('message')}")
            return None

        lat = city_data['coord']['lat']
        lon = city_data['coord']['lon']
        temperature = city_data['main']['temp']  # Get temperature in Celsius
        humidity = city_data['main']['humidity']  # Get humidity in %

        # Fetch air quality data
        air_quality_url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}"
        air_quality_data = requests.get(air_quality_url).json()

        return air_quality_data, temperature, humidity
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Function to simulate predicted weather conditions
def simulate_weather_forecast():
    conditions = ['Sunny', 'Cloudy', 'Rain', 'Overcast', 'Thunder', 'Partly Sunny', 'Fog', 'Showers', 'Snowy', 'Clear Night']
    return random.choices(conditions, k=10)

# Function to simulate accuracy data
def simulate_accuracy():
    return random.uniform(80, 100)  # Simulated accuracy between 80% to 100%

# Function to categorize air quality
def categorize_air_quality(aqi):
    if aqi <= 50:
        return "Good", 40  # Example percentage for "Good"
    elif aqi <= 100:
        return "Moderate", 30  # Example percentage for "Moderate"
    elif aqi <= 150:
        return "Compromised Risk", 15  # Example percentage for "Compromised Risk"
    elif aqi <= 200:
        return "Unhealthy", 10  # Example percentage for "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy", 4  # Example percentage for "Very Unhealthy"
    else:
        return "Hazardous", 1  # Example percentage for "Hazardous"

# Dash Layout
app.layout = html.Div(
    style={'backgroundColor': '#1e1e1e', 'padding': '20px'},  # Dark background
    children=[
        html.H1("Atmospheric Insight Engine",
                style={'text-align': 'center', 'color': 'cyan', 'font-size': '80px'}),

        # Input for city search
        dcc.Input(id="city-input", type="text", placeholder="Enter city name", value='Bhopal',
                  style={'fontSize': '24px', 'width': '30%', 'padding': '20px', 'margin-bottom': '20px',
                         'display': 'block', 'margin': '0 auto', 'border-radius': '5px', 'border': '2px solid cyan'}),

        # Display real-time date and time
        html.Div(id='current-datetime',
                 style={'font-size': '30px', 'margin-bottom': '20px', 'color': 'cyan', 'text-align': 'center'}),

        # Interval component to refresh date-time and data every minute
        dcc.Interval(id='interval-component', interval=60 * 1000, n_intervals=0),

        # Dashboard layout for charts
        html.Div([
            # First row (PM2.5 and PM10 Pie Chart)
            html.Div([
                dcc.Graph(id='pm-chart', style={'display': 'inline-block', 'width': '100%', 'border': '2px solid cyan',
                                                'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                                'margin': '5px'})  # Reduced margin
            ], style={'display': 'flex', 'justify-content': 'space-between'}),

            # Second row (Line Chart for Air Components and Accuracy Chart)
            html.Div([
                dcc.Graph(id='components-line-chart',
                          style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                 'margin': '5px'}),  # Reduced margin
                dcc.Graph(id='accuracy-chart',
                          style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                 'margin': '5px'})  # Reduced margin
            ], style={'display': 'flex', 'justify-content': 'space-between'}),

            # Third row (Temperature and Humidity Gauges)
            html.Div([
                dcc.Graph(id='temp-chart', style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                                  'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                                  'margin': '5px'}),  # Reduced margin
                dcc.Graph(id='humidity-chart',
                          style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                 'margin': '5px'})  # Reduced margin
            ], style={'display': 'flex', 'justify-content': 'space-between'}),

            # Fourth row (Predicted Weather Conditions and Air Quality Categories)
            html.Div([
                dcc.Graph(id='weather-forecast-chart',
                          style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                 'margin': '5px'}),  # Reduced margin
                dcc.Graph(id='air-quality-chart',
                          style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                 'margin': '5px'})  # Reduced margin
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
        ]),

        # Footer with developer info
        html.Footer(
            style={'text-align': 'center', 'margin-top': '20px', 'color': 'cyan'},
            children=[
                html.Div("Developed by Shubham Rahangdale", style={'font-size': '35px'}),
                html.Div("© 2024 All Rights Reserved", style={'font-size': '20px'})
            ]
        )
    ]
)

# Update current date and time
@app.callback(
    Output('current-datetime', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_time(n):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"Current Date and Time: {now}"

# Update charts based on city input
@app.callback(
    [Output('pm-chart', 'figure'),
     Output('components-line-chart', 'figure'),
     Output('accuracy-chart', 'figure'),
     Output('temp-chart', 'figure'),
     Output('humidity-chart', 'figure'),
     Output('weather-forecast-chart', 'figure'),
     Output('air-quality-chart', 'figure')],
    [Input('city-input', 'value'), Input('interval-component', 'n_intervals')]
)
def update_charts(city, n):
    result = get_air_quality_and_weather(city)

    if result is None:
        # Return empty figures if data fetch failed
        return [go.Figure()] * 7

    air_quality_data, temperature, humidity = result

    components = air_quality_data['list'][0]['components']
    aqi = air_quality_data['list'][0]['main']['aqi']
    air_quality_label, percentage = categorize_air_quality(aqi)

    # Pie chart for PM2.5 and PM10
    # Pie chart for PM2.5 and PM10
    pm_data = {'PM2.5': components['pm2_5'], 'PM10': components['pm10']}
    pm_chart = px.pie(
        values=pm_data.values(),
        names=pm_data.keys(),
        title='PM2.5 and PM10 Distribution',
        color_discrete_sequence=['#05d7ef', '#343d3d']  # Custom colors for the pie chart segments
    )
    pm_chart.update_traces(textinfo='percent+label', textfont=dict(color='white'))
    pm_chart.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')

    )

    # Line chart for air components
    air_components_chart = go.Figure()
    air_components_chart.add_trace(go.Scatter(x=list(components.keys()), y=list(components.values()), mode='lines+markers',
                                                marker=dict(color='cyan')))
    air_components_chart.update_layout(title='Air Quality Components', xaxis_title='Components', yaxis_title='Concentration (µg/m³)',
                                       paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))

    # Simulated accuracy data
    accuracy_data = [simulate_accuracy() for _ in range(10)]  # Simulate accuracy data for the last 10 minutes
    accuracy_chart = go.Figure()
    accuracy_chart.add_trace(go.Scatter(x=list(range(10)), y=accuracy_data, mode='lines+markers',
                                          marker=dict(color='cyan'), name='Accuracy'))
    accuracy_chart.update_layout(title='Real-time Accuracy Chart', xaxis_title='Time (minutes)', yaxis_title='Accuracy (%)',
                                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))

    # Temperature gauge
    temp_chart = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temperature,
        title={'text': "Temperature (°C)", 'font': {'color': 'white'}},
        gauge={'axis': {'range': [None, 50]}, 'bar': {'color': 'cyan'}, 'bgcolor': 'rgba(0,0,0,0)'}
    ))
    temp_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))

    # Humidity gauge
    humidity_chart = go.Figure(go.Indicator(
        mode="gauge+number",
        value=humidity,
        title={'text': "Humidity (%)", 'font': {'color': 'white'}},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': 'cyan'}, 'bgcolor': 'rgba(0,0,0,0)'}
    ))
    humidity_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))

    # Forecast chart
    predicted_weather = simulate_weather_forecast()
    weather_forecast_chart = go.Figure(data=[
        go.Bar(x=list(range(10)), y=predicted_weather, marker_color='cyan')
    ])
    weather_forecast_chart.update_layout(title='Predicted Weather Conditions', xaxis_title='Time', yaxis_title='Condition',
                                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))

    # Air Quality Category Chart
    air_quality_chart = go.Figure(data=[
        go.Bar(x=[air_quality_label], y=[percentage], marker_color='cyan')
    ])
    air_quality_chart.update_layout(title='Air Quality Category', xaxis_title='Category', yaxis_title='Percentage',
                                     paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))

    return pm_chart, air_components_chart, accuracy_chart, temp_chart, humidity_chart, weather_forecast_chart, air_quality_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
