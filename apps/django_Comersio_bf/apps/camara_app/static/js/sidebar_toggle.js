document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.sidebar');
    const logoImg = document.getElementById('logo-sidebar');
    const body = document.body;

    if (logoImg && sidebar && body) {
        logoImg.addEventListener('click', function () {
            sidebar.classList.toggle('compact');
            body.classList.toggle('sidebar-compacted');
        });
    }
});