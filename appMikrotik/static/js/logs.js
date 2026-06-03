function mapearDatosLogs(event) {
    var detalleModal = document.getElementById('detalleLogModal');
    if (!detalleModal) return;

    var button = event.relatedTarget;
    if (!button) return;

    var nombreOperador = button.getAttribute('data-log-nombreOperador') || '';
    var mensaje = button.getAttribute('data-log-mensaje') || '';
    var modulo = button.getAttribute('data-log-modulo') || '';
    var fecha = button.getAttribute('data-log-fecha') || '';
    var error = button.getAttribute('data-log-error') || '';

    var nombreInput = detalleModal.querySelector('#detalle-log-nombreOperador');
    if (nombreInput) nombreInput.value = nombreOperador;

    var mensajeInput = detalleModal.querySelector('#detalle-log-mensaje');
    if (mensajeInput) mensajeInput.value = mensaje;

    var moduloInput = detalleModal.querySelector('#detalle-log-modulo');
    if (moduloInput) moduloInput.value = modulo;

    var fechaInput = detalleModal.querySelector('#detalle-log-fecha');
    if (fechaInput) fechaInput.value = fecha;

    var errorInput = detalleModal.querySelector('#detalle-log-error');
    if (errorInput) errorInput.value = error;
}

document.addEventListener('DOMContentLoaded', function () {
    var detalleModal = document.getElementById('detalleLogModal');
    if (!detalleModal) return;

    detalleModal.addEventListener('show.bs.modal', mapearDatosLogs);
});