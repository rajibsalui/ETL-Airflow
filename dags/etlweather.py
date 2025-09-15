from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime, timedelta
import json
import requests


# latitude and longitude for London
LATITUDE ='51.5074'
LONGITUDE = '-0.1278'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days=1),
}

##DAG

with DAG(
    dag_id='etl_weather_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
) as dags:
    
    @task()
    def extract_weather_data():
        """Extract weather data from the Open-Meteo API"""
        
        http_hook = HttpHook(method='GET', http_conn_id=API_CONN_ID) # use http hook to connect to the API

        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true' # define the endpoint with parameters

        response = http_hook.run(endpoint) # run the API request

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")  
        return response.json()  # return the JSON response
    
    @task()
    def transform_weather_data(weather_data):
        """Transform the weather data"""
        current_weather = weather_data['current_weather'] # extract current weather data JSON
        transformed_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode'],
        }
        return transformed_data
    @task()
    def load_weather_data(transformed_data):
        """Load the weather data into a Postgres database"""
        postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID) # use postgres hook to connect to the database
        conn = postgres_hook.get_conn() # get the connection
        cursor = conn.cursor() # get the cursor

        # create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                weathercode INT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # insert data into the table
        cursor.execute("""
            INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode'],
        ))
        conn.commit() # commit the transaction
        cursor.close() # close the cursor
        conn.close() # close the connection


        #DAG workflow ETL pipeline
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)