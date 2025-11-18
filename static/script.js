// script.js
const STATUS_CARD = document.getElementById('status-card');
const CURRENT_STATUS_EL = document.getElementById('current-status');
const LAST_UPDATE_EL = document.getElementById('last-update');
const ALERTS_LIST_EL = document.getElementById('alerts-list');

const API_ALERTS_URL = '/api/alerts';
const ASSET_ID = "Maquina_Prensa_001"; // Deve ser injetado do back-end para ser ideal

/**
 * Busca os alertas do servidor e atualiza a interface.
 */
async function fetchAlerts() {
    try {
        const response = await fetch(API_ALERTS_URL);
        const alerts = await response.json();
        
        updateStatus(alerts.length > 0 ? alerts[0] : null);
        renderAlerts(alerts);
        
    } catch (error) {
        console.error('Erro ao buscar alertas:', error);
        CURRENT_STATUS_EL.textContent = "ERRO DE CONEXÃO";
        STATUS_CARD.className = 'card alerta';
    }
}

/**
 * Atualiza o card de status principal com base no alerta mais recente.
 * @param {object} latestAlert - O alerta mais recente ou null.
 */
function updateStatus(latestAlert) {
    const isCritical = latestAlert && latestAlert.severity === 'CRITICO';
    
    // Atualiza o estado da máquina
    if (isCritical) {
        CURRENT_STATUS_EL.textContent = "ANOMALIA CRÍTICA";
        STATUS_CARD.className = 'card critico';
    } else {
        // Se o último alerta não for crítico, assume-se que está normal.
        CURRENT_STATUS_EL.textContent = "NORMAL";
        STATUS_CARD.className = 'card normal';
    }

    // Atualiza o timestamp da última leitura
    LAST_UPDATE_EL.textContent = latestAlert 
        ? new Date(latestAlert.timestamp * 1000).toLocaleTimeString() 
        : new Date().toLocaleTimeString();
}

/**
 * Renderiza a lista de alertas.
 * @param {Array<object>} alerts - Lista de alertas.
 */
function renderAlerts(alerts) {
    if (alerts.length === 0) {
        ALERTS_LIST_EL.innerHTML = '<li>Nenhum alerta registrado ainda.</li>';
        return;
    }

    ALERTS_LIST_EL.innerHTML = alerts.map(alert => {
        const severityClass = alert.severity.toLowerCase();
        return `
            <li>
                <span>${alert.human_time} - ${alert.message}</span>
                <span class="severity-tag ${alert.severity}">${alert.severity}</span>
                <span style="font-style: italic;">(MSE: ${alert.value})</span>
            </li>
        `;
    }).join('');
}

// Inicia a busca de alertas e repete a cada 3 segundos
fetchAlerts();
setInterval(fetchAlerts, 3000); // Poll a cada 3 segundos
