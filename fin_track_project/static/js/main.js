document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => bootstrap.Alert.getOrCreateInstance(alert).close(), 5000);
    });

    document.querySelectorAll('[data-flash-messages]').forEach(container => {
        container.addEventListener('closed.bs.alert', function() {
            if (!container.querySelector('.alert')) {
                container.remove();
            }
        });
    });

    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));

    document.querySelectorAll('input[type="number"][step="0.01"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) this.value = parseFloat(this.value).toFixed(2);
        });
    });
});
