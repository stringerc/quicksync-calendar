// Custom JavaScript for OAuth Hub

// Utility functions
function showToast(message, type = 'info') {
    // Simple toast notification function
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 
                      type === 'warning' ? 'alert-warning' : 'alert-info';
    
    const toast = document.createElement('div');
    toast.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Connection status checker
function checkConnectionStatus(platform) {
    fetch(`/platform/status/${platform}/`)
        .then(response => response.json())
        .then(data => {
            // Update UI based on status
            const card = document.querySelector(`[data-platform="${platform}"]`);
            if (card) {
                const statusBadge = card.querySelector('.status-badge');
                if (statusBadge) {
                    statusBadge.className = `status-badge status-${data.status}`;
                    statusBadge.innerHTML = getStatusText(data.status);
                }
            }
        })
        .catch(error => {
            console.error('Error checking status:', error);
        });
}

function getStatusText(status) {
    const statusMap = {
        'connected': '<i class="fas fa-check-circle me-1"></i>Connected',
        'connecting': '<i class="fas fa-spinner fa-spin me-1"></i>Connecting',
        'expired': '<i class="fas fa-exclamation-triangle me-1"></i>Expired',
        'error': '<i class="fas fa-times-circle me-1"></i>Error',
        'disconnected': '<i class="fas fa-circle me-1"></i>Not Connected'
    };
    return statusMap[status] || statusMap['disconnected'];
}

// Export functions for global use
window.OAuthHub = {
    showToast,
    checkConnectionStatus
};
