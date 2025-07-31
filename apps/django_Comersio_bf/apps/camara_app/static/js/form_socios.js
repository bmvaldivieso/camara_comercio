class FormSocios {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.isSubmitting = false;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStepDisplay();
        this.initializeValidation();
        this.setupKeyboardNavigation();
    }

    bindEvents() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousStep());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextStep());
        }

        if (submitBtn) {
            submitBtn.addEventListener('click', (e) => this.handleSubmit(e));
        }

        document.querySelectorAll('.progress-step').forEach((step, index) => {
            step.addEventListener('click', () => this.goToStep(index + 1));
        });
        this.setupRealTimeValidation();
    }

    setupRealTimeValidation() {
        const inputs = document.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'ArrowLeft':
                        e.preventDefault();
                        this.previousStep();
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        this.nextStep();
                        break;
                    case 'Enter':
                        if (this.currentStep === this.totalSteps) {
                            e.preventDefault();
                            this.handleSubmit(e);
                        }
                        break;
                }
            }
        });
    }

    goToStep(stepNumber) {
        if (stepNumber < 1 || stepNumber > this.totalSteps) return;
        
        if (stepNumber > this.currentStep) {
            for (let i = this.currentStep; i < stepNumber; i++) {
                if (!this.validateStep(i)) {
                    this.showNotification('Por favor, complete correctamente todos los campos del paso actual antes de continuar.', 'warning');
                    return;
                }
            }
        }

        this.hideCurrentStep();
        this.currentStep = stepNumber;
        this.showCurrentStep();
        this.updateStepDisplay();
        this.updateProgressBar();
        this.focusFirstField();
    }

    nextStep() {
        if (this.currentStep >= this.totalSteps) return;

        if (this.validateStep(this.currentStep)) {
            this.goToStep(this.currentStep + 1);
        } else {
            this.showNotification('Por favor, complete todos los campos requeridos antes de continuar.', 'error');
        }
    }

    previousStep() {
        if (this.currentStep <= 1) return;
        this.goToStep(this.currentStep - 1);
    }

    hideCurrentStep() {
        const currentSlide = document.querySelector(`.form-slide[data-slide="${this.currentStep}"]`);
        if (currentSlide) {
            currentSlide.classList.add('slide-out-left');
            setTimeout(() => {
                currentSlide.classList.remove('active', 'slide-out-left');
            }, 300);
        }
    }

    showCurrentStep() {
        const targetSlide = document.querySelector(`.form-slide[data-slide="${this.currentStep}"]`);
        if (targetSlide) {
            setTimeout(() => {
                targetSlide.classList.add('active');
                targetSlide.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        }
    }

    updateStepDisplay() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');

        if (prevBtn) {
            prevBtn.classList.toggle('d-none', this.currentStep === 1);
        }

        if (nextBtn) {
            nextBtn.classList.toggle('d-none', this.currentStep === this.totalSteps);
        }

        if (submitBtn) {
            submitBtn.classList.toggle('d-none', this.currentStep !== this.totalSteps);
        }

        const currentStepNum = document.getElementById('currentStepNum');
        if (currentStepNum) {
            currentStepNum.textContent = this.currentStep;
        }
    }

    updateProgressBar() {
        document.querySelectorAll('.progress-step').forEach((step, index) => {
            const stepNumber = index + 1;
            
            step.classList.remove('active', 'completed');
            
            if (stepNumber === this.currentStep) {
                step.classList.add('active');
            } else if (stepNumber < this.currentStep) {
                step.classList.add('completed');
            }
        });

        this.updateProgressLine();
    }

    updateProgressLine() {
        const progressContainer = document.querySelector('.progress-bar-container');
        let progressLine = progressContainer.querySelector('.progress-line');
        
        if (!progressLine) {
            progressLine = document.createElement('div');
            progressLine.className = 'progress-line';
            progressContainer.appendChild(progressLine);
        }

        const progressPercent = ((this.currentStep - 1) / (this.totalSteps - 1)) * 100;
        progressLine.style.width = `${progressPercent}%`;
    }

    validateStep(stepNumber) {
        const step = document.querySelector(`.form-slide[data-slide="${stepNumber}"]`);
        if (!step) return false;

        const requiredFields = step.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        switch(stepNumber) {
            case 1:
                isValid = this.validatePersonalInfo(step) && isValid;
                break;
            case 2:
                isValid = this.validateBusinessInfo(step) && isValid;
                break;
            case 3:
                isValid = this.validateServicesInfo(step) && isValid;
                break;
            case 4:
                isValid = this.validateConfirmation(step) && isValid;
                break;
        }

        return isValid;
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        this.clearFieldError(field);

        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        }

        if (value && isValid) {
            switch(field.type) {
                case 'email':
                    if (!this.isValidEmail(value)) {
                        isValid = false;
                        errorMessage = 'Ingrese un email válido';
                    }
                    break;
                case 'tel':
                    if (!this.isValidPhone(value)) {
                        isValid = false;
                        errorMessage = 'Ingrese un número de teléfono válido';
                    }
                    break;
                case 'url':
                    if (!this.isValidURL(value)) {
                        isValid = false;
                        errorMessage = 'Ingrese una URL válida';
                    }
                    break;
            }

            if (field.name === 'ruc_cedula' && !this.isValidRucCedula(value)) {
                isValid = false;
                errorMessage = 'Ingrese un RUC o cédula válido';
            }
        }

        if (!isValid) {
            this.showFieldError(field, errorMessage);
        } else {
            this.showFieldSuccess(field);
        }

        return isValid;
    }

    validatePersonalInfo(step) {
        const socialMediaCheckboxes = step.querySelectorAll('input[name*="redes_sociales"]:checked');
        return true;
    }

    validateBusinessInfo(step) {
        return true;
    }

    validateServicesInfo(step) {
        const businessTypeCheckboxes = step.querySelectorAll('input[name*="tipo_negocio"]:checked');
        if (businessTypeCheckboxes.length === 0) {
            this.showNotification('Debe seleccionar al menos un tipo de negocio', 'error');
            return false;
        }
        return true;
    }

    validateConfirmation(step) {
        return true;
    }

    showFieldError(field, message) {
        field.classList.add('is-invalid');
        field.classList.remove('valid');
        
        let errorDiv = field.parentNode.querySelector('.field-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    showFieldSuccess(field) {
        field.classList.add('valid');
        field.classList.remove('is-invalid');
        this.clearFieldError(field);
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    focusFirstField() {
        setTimeout(() => {
            const currentStep = document.querySelector(`.form-slide[data-slide="${this.currentStep}"]`);
            if (currentStep) {
                const firstInput = currentStep.querySelector('input, select, textarea');
                if (firstInput) {
                    firstInput.focus();
                }
            }
        }, 400);
    }

    handleSubmit(e) {
        e.preventDefault();
        
        if (this.isSubmitting) return;

        if (!this.validateStep(this.currentStep)) {
            this.showNotification('Por favor, complete todos los campos requeridos.', 'error');
            return;
        }

        this.isSubmitting = true;
        this.showLoadingState();

        setTimeout(() => {
            document.querySelector('.registration-form').submit();
        }, 1000);
    }

    showLoadingState() {
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn) {
            submitBtn.innerHTML = '<div class="spinner"></div> Procesando...';
            submitBtn.disabled = true;
        }
    }

    showNotification(message, type = 'info') {
        const existingNotification = document.querySelector('.form-notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `form-notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${this.getNotificationIcon(type)}</span>
                <span class="notification-message">${message}</span>
            </div>
        `;

        const container = document.querySelector('.registration-container');
        container.insertBefore(notification, container.firstChild);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    isValidPhone(phone) {
        const re = /^[\d\s\-\+\(\)]{7,15}$/;
        return re.test(phone);
    }

    isValidURL(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    isValidRucCedula(value) {
        const cleaned = value.replace(/\D/g, '');
        return cleaned.length >= 10 && cleaned.length <= 13;
    }
}

const notificationStyles = `
    .form-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        max-width: 400px;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideInRight 0.3s ease-out;
    }

    .notification-info {
        background: linear-gradient(135deg, #E8EEFF 0%, #F0F4FF 100%);
        border-left: 4px solid #4A66E8;
        color: #2A3B8F;
    }

    .notification-success {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0FFF0 100%);
        border-left: 4px solid #28A745;
        color: #155724;
    }

    .notification-warning {
        background: linear-gradient(135deg, #FFF3CD 0%, #FFFBF0 100%);
        border-left: 4px solid #FFC107;
        color: #856404;
    }

    .notification-error {
        background: linear-gradient(135deg, #F8D7DA 0%, #FFF0F0 100%);
        border-left: 4px solid #DC3545;
        color: #721C24;
    }

    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .notification-icon {
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    .notification-message {
        font-weight: 500;
        flex: 1;
    }

    .field-error {
        color: #DC3545;
        font-size: 0.875rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    .is-invalid {
        border-color: #DC3545 !important;
        box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1) !important;
    }

    .progress-line {
        position: absolute;
        top: 25px;
        left: 50px;
        height: 3px;
        background: linear-gradient(135deg, #4A66E8 0%, #5B73F0 100%);
        border-radius: 2px;
        z-index: 1;
        width: 0;
        transition: width 0.5s ease;
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @media (max-width: 768px) {
        .form-notification {
            position: fixed;
            top: 10px;
            left: 10px;
            right: 10px;
            max-width: none;
        }
    }
`;

document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = notificationStyles;
    document.head.appendChild(style);
    window.formSocios = new FormSocios();
});

window.FormSocios = FormSocios;