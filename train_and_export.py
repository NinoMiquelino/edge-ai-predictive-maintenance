# train_and_export.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from sklearn.preprocessing import MinMaxScaler
import os

# --- 1. Geração de Dados de Treinamento (Simulação de Vibração Normal) ---
def generate_normal_data(samples=5000, features=10):
    """Gera dados de vibração normais para treinamento (série temporal curta)."""
    # Dados seguem uma distribuição normal com baixo ruído
    data = np.random.normal(loc=0.5, scale=0.1, size=(samples, features))
    return data.astype(np.float32)

# --- 2. Preparação de Dados ---
normal_data = generate_normal_data()

# É crucial normalizar os dados antes de treinar o Autoencoder
# Usaremos um MinMaxScaler simples (de 0 a 1)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(normal_data)

# --- 3. Criação e Treinamento do Autoencoder ---
input_dim = scaled_data.shape[1]
latent_dim = 2 # Dimensão de representação reduzida (o gargalo)

# O Autoencoder
input_layer = Input(shape=(input_dim,))
# Encoder
encoded = Dense(5, activation='relu')(input_layer)
encoded = Dense(latent_dim, activation='relu')(encoded) # Camada Latente
# Decoder
decoded = Dense(5, activation='relu')(encoded)
decoded = Dense(input_dim, activation='sigmoid')(decoded) # 'sigmoid' para manter 0-1

autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer='adam', loss='mse')

print("Iniciando treinamento do Autoencoder...")
autoencoder.fit(
    scaled_data, 
    scaled_data, 
    epochs=20, 
    batch_size=32, 
    shuffle=True, 
    verbose=0
)
print("Treinamento concluído.")

# --- 4. Exportação para TensorFlow Lite (Formato de Borda) ---
# O Autoencoder já é o modelo de "inferência"
converter = tf.lite.TFLiteConverter.from_keras_model(autoencoder)
tflite_model = converter.convert()

model_path = 'anomaly_model.tflite'
with open(model_path, 'wb') as f:
    f.write(tflite_model)

print(f"Modelo Autoencoder exportado com sucesso para: {model_path}")
print("Execute 'python edge_processor.py' com este modelo.")
