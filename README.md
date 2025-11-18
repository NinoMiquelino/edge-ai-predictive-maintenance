## 🙋‍♂️ Autor

<div align="center">
  <img src="https://avatars.githubusercontent.com/ninomiquelino" width="100" height="100" style="border-radius: 50%">
  <br>
  <strong>Onivaldo Miquelino</strong>
  <br>
  <a href="https://github.com/ninomiquelino">@ninomiquelino</a>
</div>

---

# 📈 Edge-AI Predictive Maintenance System (Manutenção Preditiva na Borda)

### 💻 Tecnologias
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![TensorFlow Lite](https://img.shields.io/badge/TensorFlow%20Lite-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## 🌟 Visão Geral do Projeto

Este projeto demonstra uma arquitetura completa de **Computação na Borda (Edge Computing)** com **Inteligência Artificial na Borda (Edge AI)**. O objetivo é simular o monitoramento de um ativo industrial (e.g., uma máquina com sensor de vibração) onde a detecção de anomalias é realizada **localmente**, minimizando a latência e o volume de dados transmitidos para o servidor central.

A IA implementada é um **Autoencoder** treinado para reconhecer o padrão de vibração normal da máquina.

## 🚀 Arquitetura (Edge First)

A arquitetura do sistema é dividida em três componentes principais:

| Componente | Função | Tecnologias Chave |
| :--- | :--- | :--- |
| **Edge Processor** | Simula a leitura do sensor, executa o modelo TFLite para detecção de anomalias (Edge AI) e envia **apenas** alertas críticos ou informações de status. | Python, TensorFlow Lite, NumPy, Requests |
| **Central Backend** | Recebe e armazena os alertas da borda via API. Serve como servidor web para a interface de monitoramento. | Python (Flask) |
| **Frontend Interface** | Painel de controle totalmente responsivo, otimizado para mobile e desktop, para visualizar o status atual da máquina e o histórico de alertas. | HTML, CSS (Flexbox/Grid), JavaScript (Fetch API) |

## 🛠️ Como Executar o Projeto

### Pré-requisitos

Você precisará ter o **Python 3.x** instalado.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/NinoMiquelino/edge-ai-predictive-maintenance.git](https://github.com/SEU_USUARIO/edge-ai-predictive-maintenance.git)
    cd edge-ai-predictive-maintenance
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # .\venv\Scripts\activate # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install Flask numpy tensorflow scikit-learn requests
    ```

### Sequência de Inicialização

**Passo 1: Treinar e Exportar o Modelo de IA (Simulação de Ambiente de Desenvolvimento)**

Este passo cria o modelo leve de IA (`anomaly_model.tflite`) que será usado na borda.
```bash
python train_and_export.py
```

Passo 2: Iniciar o Servidor Central (Backend)
​Em um terminal, inicie o servidor Flask. Ele hospedará a API e o painel de controle.

```bash
python app.py
```

Passo 3: Iniciar o Processador de Borda (Edge Device)
​Em um segundo terminal, inicie o script que simula a máquina industrial e sua IA local. Ele começará a enviar alertas (críticos ou informativos) para o servidor.

```bash
python edge_processor.py
```

Passo 4: Acessar a Interface
​Abra seu navegador em http://localhost:5000.
​
⚙️ Detalhes Técnicos
​Edge AI (Autoencoder)
​O modelo utiliza uma rede neural do tipo Autoencoder.
​Treinamento: É treinado apenas com dados de vibração normal.
​Detecção na Borda: A cada leitura, o processador calcula a Perda de Reconstrução (MSE). Se o MSE exceder um limiar (ANOMALY_THRESHOLD), o dado é classificado como anômalo e um alerta é disparado.
​Vantagem: A decisão de anomalia é feita em milissegundos localmente, sem depender da conectividade de rede (latência zero para a decisão).
​Front-end Responsivo
​O painel de controle é otimizado para dispositivos móveis:
​Utiliza Flexbox e Media Queries para garantir que a coluna de status e a lista de alertas sejam exibidas de forma clara em qualquer tamanho de tela.
​O card de status (#status-card) usa animação CSS (pulse-red) para destacar alertas críticos, chamando a atenção imediata do operador.

📁 Estrutura do Projeto

```bash
edge-ai-predictive-maintenance/
├──  app.py
├──  edge_processor.py         
├── train_and_export.py    
├──  templates/               
│       └──  index.html      
├── static/
│    ├── script.js            
│    └── styles.css          
├── README.md          
└── .gitignore                
```

---

## 🤝 Contribuições
Contribuições são sempre bem-vindas!  
Sinta-se à vontade para abrir uma [*issue*](https://github.com/NinoMiquelino/edge-ai-predictive-maintenance/issues) com sugestões ou enviar um [*pull request*](https://github.com/NinoMiquelino/edge-ai-predictive-maintenance/pulls) com melhorias.

---

## 💬 Contato
📧 [Entre em contato pelo LinkedIn](https://www.linkedin.com/in/onivaldomiquelino/)  
💻 Desenvolvido por **Onivaldo Miquelino**

---
