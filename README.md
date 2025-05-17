
# US_ACCIDENTS Database Implementation Guide

## 📋 Pré-requisitos

- **MySQL Server** (8.0+ recommended)  
- **Python 3.8+**  
- **Git** (optional)  
- Required Python packages:

  ```bash
  pip install pandas mysql-connector-python
  ```

---

## 🚀 Instruções iniciais

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

## ⚙️ Configuração

1. Edite `config_paths.py`:

   ```python
   from pathlib import Path

   BASE_PATH = Path("C:/path/to/Modelagem/data")  # 👈 Update this path

   PATHS = {
       'accidents_input': BASE_PATH / "ACCIDENTS.csv",
       'accidents_output': BASE_PATH / "accidents_inserts.sql",
       'locations_input': BASE_PATH / "LOCATIONS.csv",
       'locations_output': BASE_PATH / "locations_inserts.sql",
       # Add other paths as needed
   }
   ```

---

## 🔄 Processamento de dados

Execute os scripts na seguinte ordem:

- Airport
- Location
- Weather Conditions
- Day Periods
- Weather
- Accidents 
- Road Features

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
