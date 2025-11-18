# edge_processor.py
import numpy as np
import requests
import time
import random
import tensorflow as tf
from datetime import datetime

# --- Configurações do Dispositivo ---
MODEL_PATH = 'anomaly_model.tflite'  # Arquivo gerado por train_and_export.py
SERVER_URL = 'http://localhost:5000/api/alert'
ANOMALY_THRESHOLD = 0.005  # Limite de perda de reconstrução (MSE) para classificar como CRÍTICO
ASSET_ID = "Maquina_Prensa_001"
DATA_FEATURES = 10 # Número de recursos (e.g., diferentes leituras de vibração)

# --- Inicialização da Edge AI ---
try:
    # Carrega o modelo TFLite
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(" TensorFlow Lite Interpreter carregado com sucesso.")

except Exception as e:
    print(f" ERRO ao carregar o modelo TFLite: {e}")
    print("Certifique-se de ter executado 'python train_and_export.py' primeiro.")
    # Define detalhes de fallback para evitar falha total do script
    input_details = [{'index': 0, 'shape': (1, DATA_FEATURES), 'dtype': np.float32}]
    output_details = [{'index': 0, 'shape': (1, DATA_FEATURES), 'dtype': np.float32}]

def generate_vibration_data(is_anomaly=False):
    """
    Simula a leitura de um sensor de vibração e aplica normalização simulada.
    
    O Autoencoder foi treinado em dados normalizados (0 a 1). 
    Aqui, simulamos essa normalização.
    """
    # 1. Simula dados base normalizados (loc=0.5, representando o centro da faixa de 0 a 1)
    # shape=(1, 10) pois o modelo espera um lote de 1 amostra de 10 features
    base_data = np.random.normal(loc=0.5, scale=0.1, size=(1, DATA_FEATURES)) 
    
    if is_anomaly:
        # 2. Adiciona uma anomalia (valor fora da faixa normal de treinamento)
        # O valor é somado a uma coluna aleatória para simular um pico inesperado
        random_feature = random.randint(0, DATA_FEATURES - 1)
        base_data[0, random_feature] += random.uniform(0.5, 1.5)
        
    # 3. Garante que os valores simulados fiquem entre 0 e 1 (simulação do efeito do MinMaxScaler)
    data_point = np.clip(base_data, 0.0, 1.0) 
    
    return data_point.astype(np.float32)

def process_data_and_detect(data):
    """
    Executa o modelo TFLite no dispositivo de borda para calcular o erro de reconstrução (MSE).
    """
    try:
        interpreter.set_tensor(input_details[0]['index'], data)
        interpreter.invoke()
        
        # Pega o resultado da reconstrução
        reconstruction = interpreter.get_tensor(output_details[0]['index'])
        
        # Calcula a perda de reconstrução (Erro Quadrático Médio, MSE)
        mse = np.mean(np.square(data - reconstruction))
        
        return mse
        
    except Exception as e:
        print(f" Aviso: Falha na inferência TFLite. Usando MSE de fallback (simulado). Erro: {e}")
        # Retorna um MSE alto para garantir que a anomalia simulada ainda funcione
        return 1.0 if np.max(data) > 0.9 else 0.0001


def send_alert(data):
    """
    Envia o alerta para o servidor central (Edge -> Cloud) via API REST.
    """
    payload = {
        'asset_id': ASSET_ID,
        'timestamp': time.time(),
        'severity': data['severity'],
        'metric': 'Vibracao_MSE',
        'value': round(data['mse'], 6),
        'message': data['message']
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 200:
            print(f"    [COMUNICAÇÃO] Alerta enviado. Status: {data['severity']}")
        else:
            print(f"    [ERRO API] Erro ao enviar alerta. Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("    [ERRO REDE] Erro de conexão com o servidor. O alerta foi perdido.")


if __name__ == '__main__':
    print(f"\n---  Processador Edge AI para {ASSET_ID} iniciado ---")
    print(f"   Limite de Alerta (MSE): {ANOMALY_THRESHOLD}")
    
    while True:
        # Simula uma chance de 10% de dado anômalo
        is_anomaly_simulated = random.random() < 0.1 
        
        # 1. Aquisição e Preparação de Dados (Edge)
        data_point = generate_vibration_data(is_anomaly=is_anomaly_simulated)
        
        # 2. Processamento (Edge AI: Execução do TFLite)
        mse_loss = process_data_and_detect(data_point)
        
        is_alert = mse_loss > ANOMALY_THRESHOLD
        
        # 3. Classificação e Decisão
        if is_alert:
            severity = 'CRITICO'
            status_message = f" ANOMALIA DETECTADA! Risco de Falha. MSE: {mse_loss:.6f}"
        else:
            severity = 'INFO'
            status_message = f"Operação normal. MSE: {mse_loss:.6f}"
            
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] Leitura: {status_message}")
        
        # 4. Comunicação (Somente alertas ou INFO periódico)
        # Enviamos alertas CRÍTICOS sempre, e alertas INFO (status normal) 
        # apenas 15% das vezes para manter a rede desocupada.
        if is_alert or random.random() < 0.15: 
            send_alert({
                'severity': severity,
                'mse': mse_loss,
                'message': status_message
            })

        time.sleep(random.uniform(1, 3)) # Intervalo entre leituras
