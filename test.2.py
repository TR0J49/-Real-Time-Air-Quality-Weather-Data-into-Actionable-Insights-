import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import requests
import datetime

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


# Dash Layout
app.layout = html.Div(
    style={'backgroundColor': '#1e1e1e', 'padding': '20px'},  # Dark background
    children=[
        html.H1("Atmospheric Insight Engine",
                style={'text-align': 'center', 'color': 'cyan', 'font-size': '80px'}),

        # Input for city search
        dcc.Input(id="city-input", type="text", placeholder="Enter city name", value='Delhi',
                  style={'fontSize': '24px', 'width': '30%', 'padding': '20px', 'margin-bottom': '20px',
                         'display': 'block', 'margin': '0 auto', 'border-radius': '5px', 'border': '2px solid cyan'}),

        # Display real-time date and time
        html.Div(id='current-datetime',
                 style={'font-size': '30px', 'margin-bottom': '20px', 'color': 'cyan', 'text-align': 'center'}),

        # Interval component to refresh date-time and data every minute
        dcc.Interval(id='interval-component', interval=60 * 1000, n_intervals=0),

        # Dashboard layout for six charts
        html.Div([

            # First row (AQI Gauge and Pie Chart for PM2.5/PM10)
            html.Div([
                dcc.Graph(id='aqi-chart', style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                                 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                                 'margin': '5px'}),  # Reduced margin
                dcc.Graph(id='pm-chart', style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                                'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                                'margin': '5px'})  # Reduced margin
            ], style={'display': 'flex', 'justify-content': 'space-between'}),

            # Second row (Line Chart for Air Components and Heatmap for Weather)
            html.Div([
                dcc.Graph(id='components-line-chart',
                          style={'display': 'inline-block', 'width': '48%', 'border': '2px solid cyan',
                                 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.5)',
                                 'margin': '5px'}),  # Reduced margin
                dcc.Graph(id='heatmap-chart',
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
    [Output('aqi-chart', 'figure'),
     Output('pm-chart', 'figure'),
     Output('components-line-chart', 'figure'),
     Output('heatmap-chart', 'figure'),
     Output('temp-chart', 'figure'),
     Output('humidity-chart', 'figure')],
    [Input('city-input', 'value'), Input('interval-component', 'n_intervals')]
)
def update_charts(city, n):
    result = get_air_quality_and_weather(city)

    if result is None:
        # Return empty figures if data fetch failed
        return [go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()]

    air_quality_data, temperature, humidity = result

    aqi = air_quality_data['list'][0]['main']['aqi']
    components = air_quality_data['list'][0]['components']

    # AQI Gauge Chart
    aqi_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={'text': "Air Quality Index (AQI)", 'font': {'color': 'cyan', 'size': 20}},
        gauge={'axis': {'range': [0, 500]},
               'bar': {'color': 'green' if aqi <= 100 else 'orange' if aqi <= 200 else 'red'}}
    ))
    aqi_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='cyan'))

    # PM2.5 and PM10 Pie Chart
    pm_fig = px.pie(values=[components['pm2_5'], components['pm10']],
                    names=['PM2.5', 'PM10'],
                    title="PM2.5 vs PM10",
                    color_discrete_sequence=px.colors.sequential.Viridis)
    pm_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='cyan'))

    # Line Chart for other components
    components_fig = px.line(x=['CO', 'NO', 'NO2', 'O3', 'SO2'],
                             y=[components['co'], components['no'], components['no2'], components['o3'],
                                components['so2']],
                             title="Air Quality Components", labels={'x': 'Component', 'y': 'Concentration (μg/m³)'})
    components_fig.update_traces(line=dict(color='cyan'))
    components_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='cyan'))

    # Heatmap for temperature and humidity
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=[[temperature, humidity]],
        x=['Temperature (°C)', 'Humidity (%)'],
        y=['Current'],
        colorscale='Viridis'
    ))
    heatmap_fig.update_layout(title='Temperature and Humidity Heatmap', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font=dict(color='cyan'))

    # Temperature Gauge
    temp_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temperature,
        title={'text': "Temperature (°C)", 'font': {'color': 'cyan', 'size': 20}},
        gauge={'axis': {'range': [-30, 50]},
               'bar': {'color': 'cyan'}}
    ))
    temp_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='cyan'))

    # Humidity Gauge
    humidity_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=humidity,
        title={'text': "Humidity (%)", 'font': {'color': 'cyan', 'size': 20}},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': 'cyan'}}
    ))
    humidity_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='cyan'))

    return aqi_fig, pm_fig, components_fig, heatmap_fig, temp_fig, humidity_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
