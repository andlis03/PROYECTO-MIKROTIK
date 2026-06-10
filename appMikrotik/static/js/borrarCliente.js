document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('confirmarBorradoModal');
    if (!modal) return;

    modal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        if (!button) return;

        var deleteUrl = button.getAttribute('data-delete-url');
        var clientName = button.getAttribute('data-client-name');

        var form = modal.querySelector('#confirmarBorradoForm');
        var nameElement = modal.querySelector('#confirmarBorradoClienteNombre');

        if (form && deleteUrl) {
            form.action = deleteUrl;
        }
        if (nameElement) {
            nameElement.textContent = clientName || '';
        }
    });
});