document.addEventListener('DOMContentLoaded', function () {
    const cartSidebar = document.getElementById('cart-sidebar');
    const overlay = document.getElementById('overlay');
    const navCartSidebar = document.getElementById('nav-carrito-sidebar');
    const cartIconTopbar = document.getElementById('cart-icon-topbar');
    const closeCartSidebarBtn = document.getElementById('close-cart-sidebar');

    function openCartSidebar() {
        cargarProductosCarrito();
        cartSidebar.classList.add('open');
        overlay.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        navCartSidebar.classList.add('active');
    }

    function closeCartSidebar() {
        cartSidebar.classList.remove('open');
        overlay.classList.remove('active');
        navCartSidebar.classList.remove('active');
        document.getElementById('nav-categorias').classList.add('active');
    }

    if (navCartSidebar) {
        navCartSidebar.addEventListener('click', function (event) {
            event.preventDefault();
            openCartSidebar();
        });
    }

    if (cartIconTopbar) {
        cartIconTopbar.addEventListener('click', openCartSidebar);
    }

    if (closeCartSidebarBtn) {
        closeCartSidebarBtn.addEventListener('click', closeCartSidebar);
    }
    if (overlay) {
        overlay.addEventListener('click', closeCartSidebar);
    }

    document.querySelectorAll('.nav-links .nav-item').forEach(item => {
        item.addEventListener('click', function (event) {
            if (this.id !== 'nav-carrito-sidebar' && cartSidebar.classList.contains('open')) {
                closeCartSidebar();
            }
            document.querySelectorAll('.nav-links .nav-item').forEach(navItem => {
                navItem.classList.remove('active');
            });
            this.classList.add('active');
        });
    });

});



function cargarProductosCarrito() {
    console.log('Cargando productos del carrito...');
    const container = document.getElementById('cart-items-container');
    container.innerHTML = '';

    fetch('/carrito/')
        .then(response => {
            if (!response.ok) {
                throw new Error('No autenticado');
            }
            return response.json();
        })
        .then(data => {
            const contenedor = document.querySelector('.cart-items');
            contenedor.innerHTML = ''; 

            data.productos.forEach(producto => {
                const itemHTML = `
                    <div class="cart-item">
                        <div class="item-details">
                            <div class="item-name">${producto.titulo}</div>
                            <div class="item-price">${producto.precio}$</div>
                        </div>
                    </div>
                `;
                contenedor.insertAdjacentHTML('beforeend', itemHTML);
            });
        })
        .catch(error => {
            console.error('Error al cargar el carrito:', error);
        });
}
