# app.py
from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__, static_folder='static', template_folder='templates')

# Armazenamento de alertas na memória (para simplificar)
alerts_db = []

@app.route('/api/alert', methods=['POST'])
def receive_alert():
    """Endpoint para receber alertas do Dispositivo de Borda."""
    data = request.json
    
    # Validação básica
    if not all(k in data for k in ('asset_id', 'severity', 'timestamp')):
        return jsonify({"message": "Dados incompletos"}), 400
    
    # Formata e armazena o alerta
    alert_entry = {
        'id': len(alerts_db) + 1,
        'asset_id': data.get('asset_id'),
        'timestamp': data.get('timestamp'),
        'human_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get('timestamp'))),
        'severity': data.get('severity'),
        'metric': data.get('metric'),
        'value': data.get('value'),
        'message': data.get('message')
    }
    
    # Adiciona o alerta, mantendo apenas os 50 mais recentes
    alerts_db.append(alert_entry)
    alerts_db = alerts_db[-50:] 

    print(f" NOVO ALERTE ({data.get('severity')}): {data.get('message')} (Valor: {data.get('value')})")
    
    return jsonify({"message": "Alerta recebido com sucesso", "alert": alert_entry}), 200

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Endpoint para o Front-end buscar todos os alertas."""
    # Retorna os alertas em ordem reversa (mais recente primeiro)
    return jsonify(alerts_db[::-1]), 200

@app.route('/')
def index():
    """Serve a página principal do Front-end."""
    return render_template('index.html')

if __name__ == '__main__':
    # Certifique-se de que o servidor roda no mesmo host/porta que o edge_processor.py espera
    app.run(debug=True, host='0.0.0.0', port=5000) 
