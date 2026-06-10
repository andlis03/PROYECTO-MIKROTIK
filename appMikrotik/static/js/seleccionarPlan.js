
    document.addEventListener('DOMContentLoaded', function() {
        const planSelect = document.querySelector('#id_idPlan');
        const precioInput = document.querySelector('#id_plan_precioUSD');
        const subidaInput = document.querySelector('#id_plan_velocidad_subida');
        const bajadaInput = document.querySelector('#id_plan_velocidad_bajada');

        function actualizarDatosPlan() {
            const opcion = planSelect?.selectedOptions?.[0];
            precioInput.value = opcion?.dataset?.preciousd || '';
            subidaInput.value = opcion?.dataset?.velocidadSubida || '';
            bajadaInput.value = opcion?.dataset?.velocidadBajada || '';
        }

        if (planSelect) {
            planSelect.addEventListener('change', actualizarDatosPlan);
            actualizarDatosPlan();
        }
    });
