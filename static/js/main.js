// Common JavaScript functions

// Format date to YYYY-MM-DD
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

// Get today's date
function getToday() {
    return formatDate(new Date());
}

// Show loading spinner
function showLoading(element) {
    element.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
}

// Show error message
function showError(element, message) {
    element.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-circle"></i> ${message}</div>`;
}

// Show success message
function showSuccess(element, message) {
    element.innerHTML = `<div class="success-message"><i class="fas fa-check-circle"></i> ${message}</div>`;
}

// Confirm dialog with custom message
function confirmAction(message) {
    return confirm(message);
}

// Get URL parameters
function getUrlParameter(name) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(window.location.href);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Calculate percentage
function calculatePercentage(part, total) {
    if (total === 0) return 0;
    return Math.round((part / total) * 100);
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if user is logged in
function isUserLoggedIn() {
    return document.cookie.includes('session=') || localStorage.getItem('user_id');
}

// Redirect to login if not authenticated
function requireLogin() {
    if (!isUserLoggedIn()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Set page title
function setPageTitle(title) {
    document.title = title + ' - NutriTrack';
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Initialize tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    
    // Set active nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Add loading state to buttons
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            const button = e.target.tagName === 'BUTTON' ? e.target : e.target.closest('button');
            if (button.classList.contains('btn-primary') || button.classList.contains('btn-secondary')) {
                button.classList.add('loading');
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                setTimeout(() => {
                    button.classList.remove('loading');
                }, 2000);
            }
        }
    });
});

// Export functions for use in other scripts
window.commonFunctions = {
    formatDate,
    getToday,
    showLoading,
    showError,
    showSuccess,
    confirmAction,
    getUrlParameter,
    formatNumber,
    calculatePercentage,
    isUserLoggedIn,
    requireLogin,
    setPageTitle,
    showNotification
};