import os
import subprocess
import time
from datetime import datetime
from paths import PATHS

class TestSuiteRunner:
    def __init__(self):
        self.log_file = PATHS['logs_dir'] / 'test_suite.log'
        self.scripts_order = [
            PATHS['scripts_dir'] / 'pre_processamento.py',
            PATHS['scripts_dir'] / 'weather_conditions_inserts.py',
            PATHS['scripts_dir'] / 'day_periods_inserts.py',
            PATHS['scripts_dir'] / 'weather_inserts.py',
            PATHS['scripts_dir'] / 'airports_inserts.py',
            PATHS['scripts_dir'] / 'locations_insert.py',
            PATHS['scripts_dir'] / 'road_features_inserts.py',
            PATHS['scripts_dir'] / 'accidents_inserts.py'
        ]
        PATHS['logs_dir'].mkdir(exist_ok=True)

    def log_message(self, message):
        """Registra mensagens no log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        print(log_entry.strip())
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

    def run_script(self, script_name):
        """Executa um script individual"""
        script_path = os.path.join(PATHS['scripts_dir'], script_name)
        if not os.path.exists(script_path):
            self.log_message(f"ERRO: Script não encontrado - {script_path}")
            return False

        self.log_message(f"Iniciando execução de {script_name}...")
        start_time = time.time()

        try:
            result = subprocess.run(
                ['python', script_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            elapsed = time.time() - start_time
            self.log_message(f"{script_name} concluído com sucesso em {elapsed:.2f}s")
            self.log_message(f"Saída:\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            elapsed = time.time() - start_time
            self.log_message(f"ERRO em {script_name} após {elapsed:.2f}s")
            self.log_message(f"Saída de erro:\n{e.stderr}")
            return False

    def run_suite(self):
        """Executa todos os scripts na ordem definida"""
        self.log_message("Iniciando suíte de testes...")
        success = True

        for script in self.scripts_order:
            if not self.run_script(script):
                self.log_message(f"Suíte interrompida devido a falha em {script}")
                success = False
                break

        if success:
            self.log_message("Suíte de testes concluída com SUCESSO")
        else:
            self.log_message("Suíte de testes concluída com FALHAS")

        return success

if __name__ == "__main__":
    runner = TestSuiteRunner()
    runner.run_suite()