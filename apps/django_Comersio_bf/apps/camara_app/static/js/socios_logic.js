document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;
    const bottomFloatingBarSocio = document.querySelector('.bottom-floating-bar-socio');
    const socioListButton = document.getElementById('btn-socio-list');
    const socioFormsButton = document.getElementById('btn-socio-forms');

    if (bottomFloatingBarSocio && socioListButton && socioFormsButton) {
        if (currentPath.includes('/admin_socios_formularios')) {
            socioListButton.classList.remove('active');
            socioFormsButton.classList.add('active');
        } else if (currentPath.includes('/admin_socios')) {
            socioListButton.classList.add('active');
            socioFormsButton.classList.remove('active');
        }

        socioListButton.addEventListener('click', function () {
            if (!this.classList.contains('active')) {
                window.location.href = '/admin_socios';
            }
        });

        socioFormsButton.addEventListener('click', function () {
            if (!this.classList.contains('active')) {
                window.location.href = '/admin_socios_formularios';
            }
        });
    }

    const navSociosAdmin = document.getElementById('nav-socios-admin');
    const navItemsAdmin = document.querySelectorAll('.sidebar-admin .nav-links .nav-item');
    const sectionTitleAdmin = document.getElementById('section-title-admin');

    if (currentPath.includes('/admin_socios') || currentPath.includes('/admin_socios_formularios')) {
        if (navSociosAdmin) {
            navItemsAdmin.forEach(item => item.classList.remove('active'));
            navSociosAdmin.classList.add('active');
            if (sectionTitleAdmin) {
                sectionTitleAdmin.textContent = navSociosAdmin.querySelector('span').textContent;
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

    else if (currentPath.includes('/admin_usuarios') || currentPath.includes('/admin_usuarios_incremento')) {
        const navUsuariosAdmin = document.getElementById('nav-usuarios-admin');
        if (navUsuariosAdmin) {
            navItemsAdmin.forEach(item => item.classList.remove('active'));
            navUsuariosAdmin.classList.add('active');
            if (sectionTitleAdmin) {
                sectionTitleAdmin.textContent = navUsuariosAdmin.querySelector('span').textContent;
            }
        }
    }
});