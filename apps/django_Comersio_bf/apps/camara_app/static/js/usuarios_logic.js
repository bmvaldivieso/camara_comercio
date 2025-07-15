document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;
    const bottomFloatingBar = document.querySelector('.bottom-floating-bar');
    const userListButton = document.getElementById('btn-user-list');
    const userIncrementButton = document.getElementById('btn-user-increment');

    if (userListButton && userIncrementButton) {
        if (currentPath.includes('/admin_usuarios_incremento')) {
            userListButton.classList.remove('active');
            userIncrementButton.classList.add('active');
        } else if (currentPath.includes('/admin_usuarios')) {
            userListButton.classList.add('active');
            userIncrementButton.classList.remove('active');
        }

        userListButton.addEventListener('click', function () {
            if (!this.classList.contains('active')) {
                window.location.href = '/admin_usuarios';
            }
        });

        userIncrementButton.addEventListener('click', function () {
            if (!this.classList.contains('active')) {
                window.location.href = '/admin_usuarios_incremento';
            }
        });
    }

    const filterButtons = document.querySelectorAll('.filter-button');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function () {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                console.log(`Filtro "${this.textContent.trim()}" aplicado.`);
            });
        });

        if (filterButtons[0]) {
            filterButtons[0].classList.add('active');
        }
    }

    const navUsuariosAdmin = document.getElementById('nav-usuarios-admin');
    const navItemsAdmin = document.querySelectorAll('.sidebar-admin .nav-links .nav-item');
    const sectionTitleAdmin = document.getElementById('section-title-admin');

    if (currentPath.includes('/admin_usuarios') || currentPath.includes('/admin_usuarios_incremento')) {
        if (navUsuariosAdmin) {
            navItemsAdmin.forEach(item => item.classList.remove('active'));
            navUsuariosAdmin.classList.add('active');
            if (sectionTitleAdmin) {
                sectionTitleAdmin.textContent = navUsuariosAdmin.querySelector('span').textContent;
            }
        }
    } else if (currentPath.includes('/dashboard')) {
        const navDashboardAdmin = document.getElementById('nav-dashboard-admin');
        if (navDashboardAdmin) {
            navItemsAdmin.forEach(item => item.classList.remove('active'));
            navDashboardAdmin.classList.add('active');
            if (sectionTitleAdmin) {
                sectionTitleAdmin.textContent = navDashboardAdmin.querySelector('span').textContent;
            }
        }
    }
});