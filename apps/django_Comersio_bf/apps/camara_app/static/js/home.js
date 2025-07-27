// Sample publications data
const samplePublications = [
    {
        id: 1,
        titulo: "Servicios de Consultoría Empresarial",
        contenido: "Ofrecemos servicios especializados de consultoría para el crecimiento y desarrollo de su empresa. Nuestro equipo de expertos le ayudará a optimizar sus procesos y aumentar su rentabilidad.",
        servicio: "consultoria",
        fecha_creacion: "2024-01-15",
        imagenes: []
    },
    {
        id: 2,
        titulo: "Capacitación en Marketing Digital",
        contenido: "Programa completo de capacitación en marketing digital para empresarios y emprendedores. Aprenda las mejores estrategias para promocionar su negocio en línea.",
        servicio: "capacitacion",
        fecha_creacion: "2024-01-10",
        imagenes: []
    },
    {
        id: 3,
        titulo: "Productos Artesanales de Calidad",
        contenido: "Ofrecemos una amplia gama de productos artesanales elaborados por artesanos locales. Calidad garantizada y precios competitivos para mayoristas y minoristas.",
        servicio: "comercio",
        fecha_creacion: "2024-01-08",
        imagenes: []
    }
];

// DOM Elements
const publicationForm = document.getElementById('publicationForm');
const imageInput = document.getElementById('imagenes');
const imagePreview = document.getElementById('imagePreview');
const publicationsGrid = document.getElementById('publicationsGrid');
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    displayPublications();
    setupSmoothScrolling();
    setupScrollAnimation();
}

function setupEventListeners() {
    // Form submission
    if (publicationForm) {
        publicationForm.addEventListener('submit', handleFormSubmission);
    }

    // Image upload
    if (imageInput) {
        imageInput.addEventListener('change', handleImageUpload);
    }

    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', toggleMobileMenu);
    }

    // File upload area drag and drop
    const fileUploadArea = document.getElementById('fileUploadArea');
    if (fileUploadArea) {
        fileUploadArea.addEventListener('dragover', handleDragOver);
        fileUploadArea.addEventListener('drop', handleDrop);
        fileUploadArea.addEventListener('click', () => imageInput.click());
    }
}

function handleFormSubmission(e) {
    e.preventDefault();
    
    const formData = new FormData(publicationForm);
    const publicationData = {
        id: Date.now(),
        titulo: formData.get('titulo'),
        contenido: formData.get('contenido'),
        servicio: formData.get('servicio'),
        fecha_creacion: new Date().toISOString().split('T')[0],
        imagenes: []
    };

    // Handle images
    const files = imageInput.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();
        reader.onload = function(e) {
            publicationData.imagenes.push(e.target.result);
            if (publicationData.imagenes.length === files.length) {
                addPublication(publicationData);
            }
        };
        reader.readAsDataURL(file);
    }

    if (files.length === 0) {
        addPublication(publicationData);
    }
}

function handleImageUpload(e) {
    const files = e.target.files;
    imagePreview.innerHTML = '';

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        
        if (file.size > 5 * 1024 * 1024) {
            alert('El archivo ' + file.name + ' es demasiado grande. Máximo 5MB por imagen.');
            continue;
        }

        if (!file.type.startsWith('image/')) {
            alert('El archivo ' + file.name + ' no es una imagen válida.');
            continue;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            createImagePreview(e.target.result, i);
        };
        reader.readAsDataURL(file);
    }
}

function createImagePreview(src, index) {
    const previewItem = document.createElement('div');
    previewItem.className = 'preview-item';
    previewItem.innerHTML = `
        <img src="${src}" alt="Preview ${index + 1}">
        <button type="button" class="remove-btn" onclick="removeImage(${index})">×</button>
    `;
    imagePreview.appendChild(previewItem);
}

function removeImage(index) {
    const dt = new DataTransfer();
    const files = imageInput.files;
    
    for (let i = 0; i < files.length; i++) {
        if (i !== index) {
            dt.items.add(files[i]);
        }
    }
    
    imageInput.files = dt.files;
    handleImageUpload({ target: imageInput });
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.style.borderColor = 'var(--primary-blue)';
    e.currentTarget.style.background = 'var(--gradient-light)';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const files = e.dataTransfer.files;
    imageInput.files = files;
    handleImageUpload({ target: imageInput });
    
    e.currentTarget.style.borderColor = '#cbd5e1';
    e.currentTarget.style.background = 'transparent';
}

function addPublication(publicationData) {
    samplePublications.unshift(publicationData);
    displayPublications();
    resetForm();
    
    // Show success message
    showNotification('¡Publicación creada exitosamente!', 'success');
    
    // Scroll to publications section
    document.getElementById('publicationsGrid').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

function displayPublications() {
    if (!publicationsGrid) return;

    publicationsGrid.innerHTML = '';
    
    samplePublications.forEach(publication => {
        const publicationCard = createPublicationCard(publication);
        publicationsGrid.appendChild(publicationCard);
    });
}

function createPublicationCard(publication) {
    const card = document.createElement('div');
    card.className = 'publication-card';
    
    const serviceName = getServiceName(publication.servicio);
    const excerpt = publication.contenido.length > 150 
        ? publication.contenido.substring(0, 150) + '...'
        : publication.contenido;
    
    const imageHtml = publication.imagenes && publication.imagenes.length > 0
        ? `<img src="${publication.imagenes[0]}" alt="${publication.titulo}">`
        : `<i class="fas fa-image" style="font-size: 3rem;"></i>`;
    
    card.innerHTML = `
        <div class="publication-image">
            ${imageHtml}
        </div>
        <div class="publication-content">
            <div class="publication-meta">
                <span class="service-tag">${serviceName}</span>
                <span><i class="fas fa-calendar"></i> ${formatDate(publication.fecha_creacion)}</span>
            </div>
            <h3 class="publication-title">${publication.titulo}</h3>
            <p class="publication-excerpt">${excerpt}</p>
        </div>
    `;
    
    return card;
}

function getServiceName(serviceKey) {
    const serviceNames = {
        'consultoria': 'Consultoría',
        'capacitacion': 'Capacitación',
        'comercio': 'Comercio',
        'servicios-profesionales': 'Servicios Profesionales',
        'tecnologia': 'Tecnología',
        'otros': 'Otros'
    };
    return serviceNames[serviceKey] || 'Servicio';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function resetForm() {
    if (publicationForm) {
        publicationForm.reset();
        imagePreview.innerHTML = '';
    }
}

function toggleMobileMenu() {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
}

function setupSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed header
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
            
            // Close mobile menu if open
            if (navMenu.classList.contains('active')) {
                toggleMobileMenu();
            }
        });
    });
}

function setupScrollAnimation() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.feature-card, .service-card, .publication-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add notification styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background 0.2s;
    }
    
    .notification-close:hover {
        background: rgba(255,255,255,0.2);
    }
    
    @media (max-width: 768px) {
        .nav-menu.active {
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 1rem;
            gap: 1rem;
        }
        
        .hamburger.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .hamburger.active span:nth-child(2) {
            opacity: 0;
        }
        
        .hamburger.active span:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -6px);
        }
    }
`;
document.head.appendChild(notificationStyles);

window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'var(--white)';
        header.style.backdropFilter = 'none';
    }
});