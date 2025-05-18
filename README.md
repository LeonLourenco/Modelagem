
# 📦 Guia de Implementação do Banco de Dados US_ACCIDENTES

## 📋 Pré-requisitos

- **MySQL Workbench**
- **Python 3.8+**
- **Git** (opcional)
- **Pacotes Python necessários:**

  ```bash
  pip install pandas mysql-connector-python
  ```

---

## 🚀 Instruções iniciais

1. **Clone o repositório (opcional):**

   ```bash
   git clone https://github.com/your-username/US_ACCIDENTS.git
   cd US_ACCIDENTS
   ```

2. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv venv
   ```

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **Linux/MacOS:**

     ```bash
     source venv/bin/activate
     ```

   > 💡 Em alguns sistemas Unix com `zsh`, pode ser necessário rodar:
   > ```bash
   > source venv/bin/activate
   > ```

---

## ⚙️ Configuração

1. Edite o arquivo `Scripts/paths.py` (no Windows, o caminho pode aparecer como `Scripts\paths.py`):

   ```python
   from pathlib import Path

   # Exemplo para Windows:
   BASE_PATH = Path(r"C:\seu\caminho\para\Modelagem")

   # Exemplo para Linux/MacOS:
   # BASE_PATH = Path("/home/seu_usuario/caminho/para/Modelagem")

   PATHS = {
       # Diretórios principais
       'scripts_dir': BASE_PATH / "Scripts",
       'logs_dir': BASE_PATH / "Logs",
       'data_dir': BASE_PATH / "Data",
       # Outros diretórios conforme necessidade
   }
   ```

## 🔄 Execução da Suite

1. Para executar todo o processo de tratamento e carga dos dados, execute o script principal:

   ```bash
   python Scripts/run_suite.py
   ```

2. Após a execução, verifique os logs para acompanhar o andamento e resultado dos scripts:

   - **Linux/MacOS:** `logs/test_suite.log`
   - **Windows:** `logs\test_suite.log`

---


---

## 🛠️ Execução no MySQL Workbench

1. **Abra o arquivo SQL de criação do banco:**

   - Navegue até `data/output/create_tables.sql`
   - Execute o script no MySQL Workbench para criar todas as tabelas necessárias

2. **Insira os dados na ordem correta:**

   Acesse os arquivos em `data/output/` e execute os seguintes arquivos SQL **nesta ordem**:

   ```text
   1. weather_conditions_insert.sql
   2. day_periods_insert.sql
   3. weather_insert.sql
   4. airports_insert.sql
   5. locations_insert.sql
   6. road_features_insert.sql
   7. accidents_insert.sql
   ```

   > ❗ A ordem é importante para respeitar as restrições de chave estrangeira.

---

## ⚠️ Solução de Problemas

| Problemas                 | Soluções                                                      |
|---------------------------|---------------------------------------------------------------|
| Erros de codificação      | Verifique se os arquivos CSV estão em UTF-8                   |
| Erros de chave estrangeira| Verifique se os scripts SQL foram executados na ordem correta |
| Dados ausentes            | Certifique-se de que todos os scripts Python foram executados corretamente |

---

## 📝 Notas Finais

- O processo completo pode levar vários minutos com datasets grandes.
- Para melhor desempenho, recomenda-se:
  - 💾 **Mínimo de 8GB de RAM**
  - ⚡ **Armazenamento em SSD**
  - 📂 **Aproximadamente 2GB de espaço em disco** para a base completa.

---
