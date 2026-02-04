// FinTrack - JavaScript Principal

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => bootstrap.Alert.getOrCreateInstance(alert).close(), 5000);
    });
    
    // Tooltips
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));
    
    // Formatação de moeda
    document.querySelectorAll('input[type="number"][step="0.01"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) this.value = parseFloat(this.value).toFixed(2);
        });
    });
});
