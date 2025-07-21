document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.presentation-slide');
    const nextButton = document.getElementById('next-button');
    const startButton = document.getElementById('start-button');
    let currentSlideIndex = 0;

    // Función para mostrar un slide específico
    function showSlide(index) {
        slides.forEach((slide, i) => {
            if (i === index) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });

        // Ocultar/Mostrar botones al final
        if (index === slides.length - 1) {
            nextButton.classList.add('d-none');
            startButton.classList.remove('d-none');
        } else {
            nextButton.classList.remove('d-none');
            startButton.classList.add('d-none');
        }
    }

    // Inicializar mostrando el primer slide
    showSlide(currentSlideIndex);

    // Event listener para el botón "Siguiente"
    nextButton.addEventListener('click', function() {
        currentSlideIndex++;
        if (currentSlideIndex < slides.length) {
            showSlide(currentSlideIndex);
        }
    });
});