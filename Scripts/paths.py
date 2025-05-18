from pathlib import Path

BASE_PATH = Path(r"C:\Users\leolo\OneDrive\Documentos\Faculdade\Modelagem")

PATHS = {
    # Diretórios Principais
    'scripts_dir': BASE_PATH / "Scripts",
    'logs_dir': BASE_PATH / "Logs",
    'data_dir': BASE_PATH / "Data",
    
    # PRE-PROCESSAMENTO
    'airports_database': BASE_PATH / "data" / "input" / "airports_database.csv",
    'airports_repetidos': BASE_PATH / "data" / "input" / "airports_repetidos.csv",
    'repetidos_com_nomes': BASE_PATH / "data" / "input" / "repetidos_com_nomes.csv",
    'airports_output': BASE_PATH / "data" / "output" / "airports_output.csv",
    'indices_output': BASE_PATH / "data" / "output" / "indices_output.txt",
    
    # ACCIDENTS
    'accidents_input': BASE_PATH / "data" / "input" / "ACCIDENTS_filtrado.csv",
    'accidents_output': BASE_PATH / "data" / "output" / "ACCIDENTS_insert.sql",
    
    # AIRPORTS
    'airports_input': BASE_PATH / "data" / "input" / "AIRPORTS.csv",
    'airports_insert': BASE_PATH / "data" / "output" / "AIRPORTS_insert.sql",
    'airport_events': BASE_PATH / "data" / "output" / "AIRPORTS_events.csv",
    
    # DAY PERIODS
    'day_periods_input': BASE_PATH / "data" / "input" / "DAY_PERIODS_filtrado.csv",
    'day_periods_insert': BASE_PATH / "data" / "output" / "DAY_PERIODS_insert.sql",
    'day_periods_events': BASE_PATH / "data" / "output" / "DAY_PERIODS_events.sql",
    
    # LOCATIONS
    'locations_input': BASE_PATH / "data" / "input" / "LOCATIONS_filtrado.csv",
    'locations_insert': BASE_PATH / "data" / "output" / "LOCATIONS_insert.sql",
    'locations_input': BASE_PATH / "data" / "input" / "LOCATIONS_filtrado.csv",
    
    # ROAD FEATURES
    'road_features_input': BASE_PATH / "data" / "input" / "ROAD_FEATURES_filtrado.csv",
    'road_features_insert': BASE_PATH / "data" / "output" / "ROAD_FEATURES_insert.sql",
    'road_features_events': BASE_PATH / "data" / "output" / "ROAD_FEATURES_events.csv",
    
    # WEATHER
    'weather_input': BASE_PATH / "data" / "input" / "WEATHER_filtrado.csv",
    'weather_insert': BASE_PATH / "data" / "output" / "WEATHER_insert.sql",
    
    # WEATHER CONDITIONS
    'weather_conditions_input': BASE_PATH / "data" / "input" / "WEATHER_CONDITIONS_filtrado.csv",
    'weather_conditions_insert': BASE_PATH / "data" / "output" / "weather_conditions_inserts.sql",
    'weather_conditions_events': BASE_PATH / "data" / "output" / 'weather_events_inserts.sql'
}