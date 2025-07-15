document.addEventListener('DOMContentLoaded', function () {
    const formSteps = document.querySelectorAll('.form-steps-nav .step');
    const formSections = document.querySelectorAll('.solicitud-form-container .form-section');
    const btnSiguiente = document.querySelectorAll('.btn-siguiente');
    const btnVolver = document.querySelectorAll('.btn-volver');

    // Lógica para el campo "otros seguros de vida" (Sección I)
    const otrosSegurosSi = document.getElementById('otrosSegurosSi');
    const otrosSegurosNo = document.getElementById('otrosSegurosNo');
    const especifiqueCompanas = document.getElementById('especifiqueCompanas');

    // Lógica para los campos de peso (Sección II)
    const pesoCambioSi = document.getElementById('pesoCambioSi');
    const pesoCambioNo = document.getElementById('pesoCambioNo');
    const cuantoPesoCambio = document.getElementById('cuantoPesoCambio');
    const pesoIntencionalSi = document.getElementById('pesoIntencionalSi');
    const pesoIntencionalNo = document.getElementById('pesoIntencionalNo');
    const causaPesoCambio = document.getElementById('causaPesoCambio');

    // Lógica para alcohol y estupefacientes (Sección II)
    const alcoholSi = document.getElementById('alcoholSi');
    const alcoholNo = document.getElementById('alcoholNo');
    const cualesAlcohol = document.getElementById('cualesAlcohol');
    const cuantoDiariamenteAlcohol = document.getElementById('cuantoDiariamenteAlcohol');

    const estupefacientesSi = document.getElementById('estupefacientesSi');
    const estupefacientesNo = document.getElementById('estupefacientesNo');
    const cualesEstupefacientes = document.getElementById('cualesEstupefacientes');
    const hastaCuandoEstupefacientes = document.getElementById('hastaCuandoEstupefacientes');

    // Lógica para mujer (Sección II)
    const embarazadaSi = document.getElementById('embarazadaSi');
    const embarazadaNo = document.getElementById('embarazadaNo');
    const cuantosMesesEmbarazo = document.getElementById('cuantosMesesEmbarazo');

    // Lógica para la tabla de declaraciones (Sección II)
    const declaracionesTableBody = document.querySelector('#declaracionesTable tbody');
    const btnAgregarFila = document.querySelector('.btn-agregar-fila');

    let currentStep = 1;

    function showSection(stepNumber) {
        formSections.forEach(section => section.classList.remove('active'));
        document.getElementById(`section-${stepNumber}`).classList.add('active');

        formSteps.forEach(step => {
            const stepNum = parseInt(step.dataset.step);
            if (stepNum === stepNumber) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        currentStep = stepNumber;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    btnSiguiente.forEach(button => {
        button.addEventListener('click', function () {
            const nextStep = parseInt(this.dataset.nextStep);
            if (nextStep) {
                showSection(nextStep);
            }
        });
    });

    btnVolver.forEach(button => {
        button.addEventListener('click', function () {
            const prevStep = parseInt(this.dataset.prevStep);
            if (prevStep) {
                showSection(prevStep);
            }
        });
    });

    formSteps.forEach(stepButton => {
        stepButton.addEventListener('click', function () {
            const stepNumber = parseInt(this.dataset.step);
            showSection(stepNumber);
        });
    });

    function toggleEspecifiqueCompanas() {
        if (otrosSegurosSi && otrosSegurosSi.checked) {
            especifiqueCompanas.disabled = false;
        } else {
            especifiqueCompanas.disabled = true;
            especifiqueCompanas.value = '';
        }
    }
    if (otrosSegurosSi && otrosSegurosNo && especifiqueCompanas) {
        otrosSegurosSi.addEventListener('change', toggleEspecifiqueCompanas);
        otrosSegurosNo.addEventListener('change', toggleEspecifiqueCompanas);
        toggleEspecifiqueCompanas();
    }

    function togglePesoCambioFields() {
        if (pesoCambioSi && pesoCambioSi.checked) {
            cuantoPesoCambio.disabled = false;
            pesoIntencionalSi.disabled = false;
            pesoIntencionalNo.disabled = false;
        } else {
            cuantoPesoCambio.disabled = true;
            cuantoPesoCambio.value = '';
            pesoIntencionalSi.disabled = true;
            pesoIntencionalNo.disabled = true;
            pesoIntencionalNo.checked = true;
            causaPesoCambio.disabled = true;
            causaPesoCambio.value = '';
        }
    }
    function toggleCausaPesoCambio() {
        if (pesoIntencionalSi && pesoIntencionalSi.checked) {
            causaPesoCambio.disabled = false;
        } else {
            causaPesoCambio.disabled = true;
            causaPesoCambio.value = '';
        }
    }
    if (pesoCambioSi && pesoCambioNo && cuantoPesoCambio) {
        pesoCambioSi.addEventListener('change', togglePesoCambioFields);
        pesoCambioNo.addEventListener('change', togglePesoCambioFields);
        togglePesoCambioFields();
    }
    if (pesoIntencionalSi && pesoIntencionalNo && causaPesoCambio) {
        pesoIntencionalSi.addEventListener('change', toggleCausaPesoCambio);
        pesoIntencionalNo.addEventListener('change', toggleCausaPesoCambio);
        toggleCausaPesoCambio();
    }

    function toggleAlcoholFields() {
        if (alcoholSi && alcoholSi.checked) {
            cualesAlcohol.disabled = false;
            cuantoDiariamenteAlcohol.disabled = false;
        } else {
            cualesAlcohol.disabled = true;
            cualesAlcohol.value = '';
            cuantoDiariamenteAlcohol.disabled = true;
            cuantoDiariamenteAlcohol.value = '';
        }
    }
    if (alcoholSi && alcoholNo && cualesAlcohol && cuantoDiariamenteAlcohol) {
        alcoholSi.addEventListener('change', toggleAlcoholFields);
        alcoholNo.addEventListener('change', toggleAlcoholFields);
        toggleAlcoholFields();
    }

    function toggleEstupefacientesFields() {
        if (estupefacientesSi && estupefacientesSi.checked) {
            cualesEstupefacientes.disabled = false;
            hastaCuandoEstupefacientes.disabled = false;
        } else {
            cualesEstupefacientes.disabled = true;
            cualesEstupefacientes.value = '';
            hastaCuandoEstupefacientes.disabled = true;
            hastaCuandoEstupefacientes.value = '';
        }
    }
    if (estupefacientesSi && estupefacientesNo && cualesEstupefacientes && hastaCuandoEstupefacientes) {
        estupefacientesSi.addEventListener('change', toggleEstupefacientesFields);
        estupefacientesNo.addEventListener('change', toggleEstupefacientesFields);
        toggleEstupefacientesFields();
    }

    function toggleEmbarazoFields() {
        if (embarazadaSi && embarazadaSi.checked) {
            cuantosMesesEmbarazo.disabled = false;
        } else {
            cuantosMesesEmbarazo.disabled = true;
            cuantosMesesEmbarazo.value = '';
        }
    }
    if (embarazadaSi && embarazadaNo && cuantosMesesEmbarazo) {
        embarazadaSi.addEventListener('change', toggleEmbarazoFields);
        embarazadaNo.addEventListener('change', toggleEmbarazoFields);
        toggleEmbarazoFields();
    }

    if (btnAgregarFila && declaracionesTableBody) {
        btnAgregarFila.addEventListener('click', function () {
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td><input type="number" class="form-control form-control-sm" name="preguntaNro[]" /></td>
                <td><input type="text" class="form-control form-control-sm" name="detalle[]" /></td>
                <td><input type="text" class="form-control form-control-sm" name="cuando[]" /></td>
                <td><input type="text" class="form-control form-control-sm" name="duracion[]" /></td>
                <td><input type="text" class="form-control form-control-sm" name="secuelas[]" /></td>
                <td><input type="text" class="form-control form-control-sm" name="medicoTratante[]" /></td>
                <td><button type="button" class="btn btn-danger btn-sm btn-eliminar-fila"><i class="fas fa-times"></i></button></td>
            `;
            declaracionesTableBody.appendChild(newRow);

            newRow.querySelector('.btn-eliminar-fila').addEventListener('click', function () {
                newRow.remove();
            });
        });
    }

    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.sidebar .nav-links .nav-item');
    const navFormulario = document.getElementById('nav-formulario');

    if (currentPath.includes('/solicitud_seguro')) {
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
});