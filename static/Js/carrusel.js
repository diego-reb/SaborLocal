// Añade este script al final de tu body, preferiblemente en un archivo JS separado (ej. carousel.js)

document.addEventListener('DOMContentLoaded', () => {
    const carouselTrack = document.querySelector('.carousel-track');
    const slides = Array.from(carouselTrack.children);
    const nextButton = document.querySelector('.carousel-button.next');
    const prevButton = document.querySelector('.carousel-button.prev');
    const paginationDotsContainer = document.querySelector('.carousel-pagination');

    let slideWidth = slides[0].getBoundingClientRect().width;
    let currentIndex = 0;

    // Función para actualizar la posición del carrusel
    const moveToSlide = (track, targetSlide) => {
        track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
    };

    // Función para actualizar los puntos de paginación
    const updateDots = (currentDot, targetDot) => {
        currentDot.classList.remove('active');
        targetDot.classList.add('active');
    };

    // Función para mostrar/ocultar flechas de navegación (opcional, si quieres que no se "desborden")
    const updateArrows = (targetIndex) => {
        // En un carrusel que se repite, no es estrictamente necesario ocultar/mostrar flechas
        // Pero si no es cíclico, puedes añadir lógica aquí.
    };

    // Crear puntos de paginación
    slides.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('pagination-dot');
        dot.dataset.index = index;
        paginationDotsContainer.appendChild(dot);
    });

    const paginationDots = Array.from(paginationDotsContainer.children);
    if (paginationDots.length > 0) {
        paginationDots[0].classList.add('active'); // Activar el primer punto
    }

    // Posicionar los slides uno al lado del otro
    const setSlidePosition = (slide, index) => {
        slide.style.left = slideWidth * index + 'px';
    };
    slides.forEach(setSlidePosition);

    // Cuando se hace clic en el botón siguiente
    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % slides.length; // Ciclo infinito
        const targetSlide = slides[currentIndex];
        moveToSlide(carouselTrack, targetSlide);

        const currentDot = paginationDotsContainer.querySelector('.active');
        const targetDot = paginationDots[currentIndex];
        updateDots(currentDot, targetDot);
    });

    // Cuando se hace clic en el botón anterior
    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length; // Ciclo infinito
        const targetSlide = slides[currentIndex];
        moveToSlide(carouselTrack, targetSlide);

        const currentDot = paginationDotsContainer.querySelector('.active');
        const targetDot = paginationDots[currentIndex];
        updateDots(currentDot, targetDot);
    });

    // Cuando se hace clic en un punto de paginación
    paginationDotsContainer.addEventListener('click', e => {
        if (e.target.classList.contains('pagination-dot')) {
            const targetIndex = parseInt(e.target.dataset.index);
            currentIndex = targetIndex;
            const targetSlide = slides[targetIndex];
            moveToSlide(carouselTrack, targetSlide);

            const currentDot = paginationDotsContainer.querySelector('.active');
            updateDots(currentDot, e.target);
        }
    });

    // Ajustar el ancho del slide y reposicionar en redimensionamiento
    window.addEventListener('resize', () => {
        slideWidth = slides[0].getBoundingClientRect().width;
        slides.forEach(setSlidePosition);
        moveToSlide(carouselTrack, slides[currentIndex]); // Mover al slide actual
    });

    // Autoplay (opcional)
    const startAutoplay = () => {
        setInterval(() => {
            nextButton.click();
        }, 5000); // Cambia cada 5 segundos
    };

    // Descomenta la siguiente línea para activar el autoplay
    // startAutoplay();
});