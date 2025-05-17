from pathlib import Path

BASE_PATH = Path(r"C:\codigos\modelagem\Modelagem")

# Caminhos específicos
PATHS = {
    'input_csv': BASE_PATH / "accidents" / "ACCIDENTS_filtrado.csv",
    'output_sql': BASE_PATH / "accidents" / "accidents_inserts.sql",
    'weather_input': BASE_PATH / "weather" / "WEATHER_filtrado.csv",
    'weather_output': BASE_PATH / "weather" / "weather_inserts.sql",
    'weather_events': BASE_PATH / "weather_conditions" / "weather_events_inserts.sql",
    'period_events': BASE_PATH / "day_periods" / "period_events_inserts.sql",
    'road_features_input': BASE_PATH / "road_features" / "ROAD_FEATURES_filtrado.csv",
    'road_features_output': BASE_PATH / "road_features" / "road_features_inserts.sql",
    'weather_conditions_input': BASE_PATH / "weather_conditions" / "WEATHER_CONDITIONS_filtrado.csv",
    'weather_conditions_output': BASE_PATH / "weather_conditions" / "weather_conditions_inserts.sql",
    'locations_input': BASE_PATH / "locations" / "LOCATIONS_filtrado.csv",
    'locations_output': BASE_PATH / "locations" / "locations_inserts.sql",
    'airport_codes': BASE_PATH / "airports" / "AIRPORTS_COM_NOME.csv",
    'day_periods_input': BASE_PATH / "day_periods" / "DAY_PERIODSDAY_PERIODS_filtrado.csv",
    'day_periods_main_output': BASE_PATH / "day_periods" / "day_period_inserts.sql",
    'day_periods_events_output': BASE_PATH / "day_periods" / "period_events_inserts.sql",
    'airports_input': BASE_PATH / 'airports' / 'AIRPORTS_COM_NOME.csv',
    'indices_input': BASE_PATH / 'airports' / 'indices_sem_nome.txt',
    'airports_output': BASE_PATH / 'airports' / 'airport_inserts.sql',
    'airport_events_output': BASE_PATH / 'airports' / 'airport_events.csv',
    'weather_conditions_input': BASE_PATH / 'weather_conditions' / 'WEATHER_CONDITIONS.csv',
    'weather_input': BASE_PATH / 'weather' / 'WEATHER.csv',
    'road_features_input': BASE_PATH / 'road_features' / 'ROAD_FEATURES.csv',
    'locations_input': BASE_PATH / 'locations' / 'LOCATIONS.csv',
    'day_periods_input': BASE_PATH / 'day_periods' / 'DAY_PERIODSDAY_PERIODS.csv',
    'accidents_input': BASE_PATH / 'accidents' / 'ACCIDENTS.csv',
    'accidents_input': BASE_PATH / "accidents" / "ACCIDENTS_filtrado.csv",
    'accidents_output': BASE_PATH / "accidents" / "accidents_inserts.sql",
    'locations_output': BASE_PATH / "locations" / "locations_inserts.sql",
    'weather_output': BASE_PATH / "weather" / "weather_inserts.sql",
    'road_features_output': BASE_PATH / "road_features" / "road_features_inserts.sql"
}