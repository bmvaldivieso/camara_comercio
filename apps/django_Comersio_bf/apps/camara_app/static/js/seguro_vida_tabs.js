document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('.tab-bar .tab-button');
    const tabContentContainer = document.getElementById('tab-content-container');

    function loadTabContent(tabName) {
        fetch(`/${tabName === 'archivos-subidos' ? 'seguro_vida_archivos_subidos' :
            tabName === 'estado' ? 'seguro_vida_estado' :
                tabName === 'archivos-recibidos' ? 'seguro_vida_archivos_recibidos' : ''}`)
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
                console.error('Error cargando el contenido de la pestaña:', error);
                tabContentContainer.innerHTML = `<p>Error al cargar el contenido de ${tabName}.</p>`;
            });
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const tabName = this.dataset.tabTarget;
            loadTabContent(tabName);
        });
    });

    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.sidebar .nav-links .nav-item');
    const navCategorias = document.getElementById('nav-categorias');

    if (currentPath.includes('/seguro_vida')) {
        navItems.forEach(item => item.classList.remove('active'));
        if (navCategorias) {
            navCategorias.classList.add('active');
            const sectionTitle = document.getElementById('section-title');
            if (sectionTitle) {
                sectionTitle.textContent = navCategorias.querySelector('span').textContent;
                sectionTitle.previousElementSibling.className = '';
                sectionTitle.previousElementSibling.classList.add('fas', 'fa-th-large', 'me-2', 'icono-azul');
            }
        }
    }

    const initialTabTarget = document.querySelector('.tab-bar .tab-button.active')?.dataset.tabTarget;
    if (initialTabTarget) {
        loadTabContent(initialTabTarget);
    }
});