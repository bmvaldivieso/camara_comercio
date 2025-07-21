document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.form-slide');
    const progressSteps = document.querySelectorAll('.progress-step');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn'); // Este es tu botón de submit final

    let currentSlide = 0; // Índice del slide actual (empezando en 0)

    /**
     * Muestra un slide específico del formulario con una animación de deslizamiento.
     * @param {number} n El índice del slide a mostrar.
     * @param {string} direction La dirección de la animación ('next' para avanzar, 'prev' para retroceder).
     */
    function showSlide(n, direction = 'next') {
        // Asegúrate de que n esté dentro de los límites válidos
        if (n < 0 || n >= slides.length) {
            console.error("Índice de slide fuera de rango:", n);
            return;
        }

        // Ocultar todos los slides y remover clases de animación
        slides.forEach(slide => {
            slide.classList.remove('active', 'animate-left', 'animate-right');
            slide.style.display = 'none'; // Oculta para que no ocupe espacio
        });

        // Actualizar la barra de progreso
        progressSteps.forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index < n) {
                step.classList.add('completed'); // Marcar pasos previos como completados
            }
            if (index === n) {
                step.classList.add('active'); // Marcar el paso actual como activo
            }
        });

        // Mostrar el slide actual y aplicar animación
        slides[n].style.display = 'block';
        // Esto añade la clase de animación para que la transición ocurra
        requestAnimationFrame(() => { // Usa requestAnimationFrame para asegurar que el display: block se aplique antes de la animación
            if (direction === 'next') {
                slides[n].classList.add('active', 'animate-right');
            } else {
                slides[n].classList.add('active', 'animate-left');
            }
        });

        // Remover las clases de animación después de que termine la transición
        slides[n].addEventListener('transitionend', function handler() {
            slides[n].classList.remove('animate-left', 'animate-right');
            slides[n].removeEventListener('transitionend', handler);
        }, { once: true }); // { once: true } asegura que el listener se ejecute una sola vez

        // Actualizar la visibilidad de los botones de navegación
        prevBtn.classList.toggle('d-none', n === 0); // Ocultar 'Anterior' en el primer slide
        nextBtn.classList.toggle('d-none', n === slides.length - 1); // Ocultar 'Siguiente' en el último slide
        submitBtn.classList.toggle('d-none', n !== slides.length - 1); // Mostrar 'Registrarme' solo en el último slide

        // *** IMPORTANTE: Se elimina la llamada a populateSummary() aquí ***
        // Si en el futuro quieres un resumen, deberás actualizar esta función
        // para que acceda a los valores correctos de los formularios de Django
        // y los IDs de los elementos donde mostrar el resumen.
    }

    /**
     * Avanza al siguiente slide si la validación del slide actual es exitosa.
     */
    function nextSlide() {
        if (!validateCurrentSlide()) {
            return false; // Detener la navegación si la validación falla
        }
        if (currentSlide < slides.length - 1) {
            currentSlide++;
            showSlide(currentSlide, 'next');
        }
    }

    /**
     * Retrocede al slide anterior.
     */
    function prevSlide() {
        if (currentSlide > 0) {
            currentSlide--;
            showSlide(currentSlide, 'prev');
        }
    }

    /**
     * Realiza una validación básica de los campos requeridos en el slide actual.
     * Añade/remueve la clase 'is-invalid' de Bootstrap para retroalimentación visual.
     * @returns {boolean} true si todos los campos requeridos son válidos, false en caso contrario.
     */
    function validateCurrentSlide() {
        // Asegúrate de que los inputs required tienen los IDs correctos si no son generados por Django
        // Si estás usando los forms de Django, los IDs serán 'id_nombre_del_campo'.
        // Tu código de forms.py ya asigna los IDs de tu HTML original a los widgets,
        // así que 'id_razon_social', 'id_email', etc., no deberían usarse en JS directamente,
        // sino los IDs que definiste ('razon_social', 'email').

        const currentInputs = slides[currentSlide].querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        let firstInvalidInput = null;

        currentInputs.forEach(input => {
            // Especialmente para checkboxes o radios, la validación de .value.trim() no es suficiente.
            // Aquí se valida que tengan un valor, lo cual funciona para text, email, number, date, etc.
            if (input.type === 'checkbox' || input.type === 'radio') {
                // Para checkboxes/radios, si son requeridos, debes asegurarte de que al menos uno esté seleccionado en su grupo.
                // Esta lógica sería más compleja y debería ir por grupo de nombre (name="redes[]", name="tipo_negocio[]")
                // Por ahora, asumimos que input.value.trim() es suficiente para otros tipos.
            } else if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
                if (!firstInvalidInput) {
                    firstInvalidInput = input;
                }
            } else {
                input.classList.remove('is-invalid');
            }
        });

        // Validación específica para el campo de email (asumiendo que está en el primer slide)
        // Usamos el ID que le asignamos en el forms.py: 'email'
        if (currentSlide === 0) {
            const emailInput = document.getElementById('email'); // Usar 'email', no 'id_email'
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailInput && emailInput.hasAttribute('required') && !emailRegex.test(emailInput.value.trim())) {
                emailInput.classList.add('is-invalid');
                isValid = false;
                if (!firstInvalidInput) {
                    firstInvalidInput = emailInput;
                }
            } else if (emailInput) {
                emailInput.classList.remove('is-invalid');
            }
        }

        // Si hay campos inválidos, enfocar el primero y mostrar alerta
        if (!isValid) {
            if (firstInvalidInput) {
                firstInvalidInput.focus();
            }
            // Muestra una alerta solo si la validación JS falla,
            // pero recuerda que Django también validará al hacer submit.
            alert('Por favor, completa correctamente todos los campos requeridos antes de continuar.');
        }
        return isValid;
    }

    // *** ELIMINAMOS LA FUNCIÓN populateSummary() YA QUE NO ES NECESARIA CON LA ESTRUCTURA ACTUAL ***
    /*
    function populateSummary() {
        // ... (todo el contenido de la función populateSummary) ...
    }
    */

    // --- Listeners de Eventos ---

    // Listener para el botón "Siguiente"
    nextBtn.addEventListener('click', nextSlide);

    // Listener para el botón "Anterior"
    prevBtn.addEventListener('click', prevSlide);

    // Listeners para los pasos de la barra de progreso (clic)
    progressSteps.forEach((step, index) => {
        step.addEventListener('click', () => {
            // Permitir ir a pasos anteriores sin validación estricta
            if (index < currentSlide) {
                currentSlide = index;
                showSlide(currentSlide, 'prev');
            }
            // Permitir ir a pasos posteriores solo si el slide actual es válido
            else if (index > currentSlide) {
                 if (validateCurrentSlide()) { // Valida el slide actual antes de avanzar
                    currentSlide = index;
                    showSlide(currentSlide, 'next');
                 }
            }
            // Si hace clic en el paso actual, no hacer nada
        });
    });


     submitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (validateCurrentSlide()) {
            e.target.form.submit();
        }
     });


    // Inicializar el formulario mostrando el primer slide
    showSlide(currentSlide);
});