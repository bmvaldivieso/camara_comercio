document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('.form-tab-bar .form-tab-button');
    const tabContentContainer = document.getElementById('form-tab-content-container');


    function loadFormTabContent(tabName) {
        const urlMap = {
            'formulario-a': '/formularios_form_a',
            'formulario-b': '/formularios_form_b',
        };

        const url = urlMap[tabName];

        if (!url) {
            console.error('No se encontró una URL asociada a', tabName);
            return;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                tabContentContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('Error cargando el contenido del formulario:', error);
                tabContentContainer.innerHTML = `<p>Error al cargar el contenido de ${tabName}.</p>`;
            });
    }


    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const tabName = this.dataset.tabTarget;
            loadFormTabContent(tabName);
        });
    });

    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.sidebar .nav-links .nav-item');
    const navFormulario = document.getElementById('nav-formulario');
    if (currentPath.includes('/formularios')) {
        navItems.forEach(item => item.classList.remove('active'));
        if (navFormulario) {
            navFormulario.classList.add('active');
            const sectionTitle = document.getElementById('section-title');
            if (sectionTitle) {
                sectionTitle.textContent = navFormulario.querySelector('span').textContent;
                const iconElement = sectionTitle.previousElementSibling;
                if (iconElement) {
                    iconElement.className = '';
                    iconElement.classList.add('far', 'fa-file-alt', 'me-2', 'icono-azul');
                }
            }
        }
    }

    const initialTabTarget = document.querySelector('.form-tab-bar .form-tab-button.active')?.dataset.tabTarget;
    if (initialTabTarget) {
        loadFormTabContent(initialTabTarget);
    }
});