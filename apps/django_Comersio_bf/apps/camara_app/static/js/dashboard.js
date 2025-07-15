document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.chart-card .dropdown select, .list-card .dropdown select').forEach(select => {
        select.addEventListener('change', function () {
            console.log(`Selector "${this.previousElementSibling.textContent.trim()}" cambió a: ${this.value}`);
        });
    });
});