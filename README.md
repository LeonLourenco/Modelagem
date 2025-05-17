
# US_ACCIDENTS Database Implementation Guide

## 📋 Prerequisites

- **MySQL Server** (8.0+ recommended)  
- **Python 3.8+**  
- **Git** (optional)  
- Required Python packages:

  ```bash
  pip install pandas mysql-connector-python
  ```

---

## 🚀 Setup Instructions

1. **Clone the repository (optional)**

   ```bash
   git clone https://github.com/your-username/US_ACCIDENTS.git
   cd US_ACCIDENTS
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   ```

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **Linux/Mac:**

     ```bash
     source venv/bin/activate
     ```

---

## 🗂 Project Structure

```
📦US_ACCIDENTS
├── 📂data
│   ├── ACCIDENTS.csv
│   ├── LOCATIONS.csv
│   ├── WEATHER.csv
│   ├── ROAD_FEATURES.csv
│   └── ...
├── 📂scripts
│   ├── create_tables.sql
│   ├── config_paths.py
│   ├── process_accidents.py
│   ├── process_locations.py
│   └── ...
└── README.md
```

---

## ⚙️ Configuration

1. Edit `scripts/config_paths.py`:

   ```python
   from pathlib import Path

   BASE_PATH = Path("C:/path/to/US_ACCIDENTS/data")  # 👈 Update this path

   PATHS = {
       'accidents_input': BASE_PATH / "ACCIDENTS.csv",
       'accidents_output': BASE_PATH / "accidents_inserts.sql",
       'locations_input': BASE_PATH / "LOCATIONS.csv",
       'locations_output': BASE_PATH / "locations_inserts.sql",
       # Add other paths as needed
   }
   ```

---

## 🔄 Data Processing Pipeline

Execute os scripts na seguinte ordem:

1. **Weather Conditions**

   ```bash
   python scripts/process_weather_conditions.py
   ```

2. **Day Periods**

   ```bash
   python scripts/process_day_periods.py
   ```

3. **Airports**

   ```bash
   python scripts/process_airports.py
   ```

4. **Locations**

   ```bash
   python scripts/process_locations.py
   ```

5. **Road Features**

   ```bash
   python scripts/process_road_features.py
   ```

6. **Accidents (Final step)**

   ```bash
   python scripts/process_accidents.py
   ```

---

## 🗄 Database Import

1. **Create the database**

   ```sql
   CREATE SCHEMA `US_ACCIDENTS` DEFAULT CHARACTER SET utf8mb4;
   USE US_ACCIDENTS;
   ```

2. **Execute SQL scripts in this exact order:**

   ```sql
   SOURCE data/weather_conditions_inserts.sql;
   SOURCE data/day_periods_inserts.sql;
   SOURCE data/airport_inserts.sql;
   SOURCE data/locations_inserts.sql;
   SOURCE data/road_features_inserts.sql;
   SOURCE data/accidents_inserts.sql;
   ```

---

## ✅ Verification

```sql
-- Check data counts
SELECT COUNT(*) FROM ACCIDENTS;
SELECT COUNT(*) FROM LOCATIONS;

-- Sample data check
SELECT * FROM WEATHER LIMIT 5;
```

---

## ⚠️ Troubleshooting

| Issue                 | Solution                                           |
|----------------------|----------------------------------------------------|
| Encoding errors       | Ensure all CSV files are UTF-8 encoded            |
| Foreign key errors    | Verify scripts were executed in correct order     |
| Missing data          | Check Python scripts converted NULL values properly |
| Connection issues     | Verify MySQL server is running                    |

---

## 📝 Notes

- O processo completo pode levar vários minutos com datasets grandes.
- Para melhor desempenho, considere:

  - Mínimo de 8GB de RAM  
  - Armazenamento em SSD  
  - Aproximadamente 2GB de espaço em disco são necessários para a base completa.

---

**✅ Este guia inclui:**

- Pré-requisitos claros  
- Instruções de instalação  
- Visualização da estrutura do projeto  
- Etapas de configuração  
- Pipeline ordenado de processamento  
- Importação da base de dados  
- Verificação e checagem de dados  
- Tabela de problemas comuns  
- Notas úteis sobre performance  


