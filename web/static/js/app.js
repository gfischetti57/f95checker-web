// F95Checker Web App JavaScript

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main .container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// API helper functions
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Errore sconosciuto');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Game management
async function addGame(url) {
    try {
        await apiRequest('/api/games', {
            method: 'POST',
            body: JSON.stringify({ url })
        });
        
        showAlert('Gioco aggiunto con successo!', 'success');
        setTimeout(() => location.reload(), 1000);
    } catch (error) {
        showAlert(`Errore: ${error.message}`, 'danger');
    }
}

async function deleteGame(gameId) {
    if (!confirm('Sei sicuro di voler rimuovere questo gioco?')) return;
    
    try {
        await apiRequest(`/api/games/${gameId}`, { method: 'DELETE' });
        showAlert('Gioco rimosso con successo!', 'success');
        setTimeout(() => location.reload(), 1000);
    } catch (error) {
        showAlert(`Errore: ${error.message}`, 'danger');
    }
}

async function checkUpdates() {
    const btn = event.target;
    const originalContent = btn.innerHTML;
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Controllo...';
    
    try {
        const result = await apiRequest('/api/check-updates', { method: 'POST' });
        showAlert(result.message, result.updates_found > 0 ? 'success' : 'info');
        
        if (result.updates_found > 0) {
            setTimeout(() => location.reload(), 2000);
        }
    } catch (error) {
        showAlert(`Errore: ${error.message}`, 'danger');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalContent;
    }
}

// User registration
async function registerUser(userData) {
    try {
        await apiRequest('/api/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        
        showAlert('Utente registrato con successo!', 'success');
        return true;
    } catch (error) {
        showAlert(`Errore: ${error.message}`, 'danger');
        return false;
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Auto-refresh every 5 minutes
    setInterval(() => {
        if (document.visibilityState === 'visible') {
            location.reload();
        }
    }, 300000);
    
    // Handle form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Handle form submission based on form ID
        });
    });
});

// Service Worker registration for notifications (if supported)
if ('serviceWorker' in navigator && 'PushManager' in window) {
    navigator.serviceWorker.register('/static/js/sw.js')
        .then(registration => {
            console.log('Service Worker registered:', registration);
        })
        .catch(error => {
            console.log('Service Worker registration failed:', error);
        });
}