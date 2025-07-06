// Glavni JavaScript fajl za Shopping List aplikaciju

document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltip inicijalizacija
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss za flash poruke
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Automatski se zatvara nakon 5 sekundi
    });
    
    // Potvrda za brisanje stavki
    const deleteButtons = document.querySelectorAll('form[onsubmit]');
    deleteButtons.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Da li ste sigurni da želite obrisati ovu stavku?')) {
                e.preventDefault();
                return false;
            }
        });
    });
});
