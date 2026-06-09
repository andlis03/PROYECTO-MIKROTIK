
  const usdEntrada = document.getElementById('id_montoUSD');
  const bsEntrada = document.getElementById('monto_bs');
  const tasaEntrada = document.getElementById('id_tasa');

  function pasar_Decimal(value) {
    if (!value) return 0;
    return parseFloat(value.toString().replace(/\s+/g, '').replace(',', '.')) || 0;
  }


  function sanitizeNumericInput(input) {
    if (!input) return;
    let val = input.value || '';
    const cursor = input.selectionStart || 0;

    // reemplazar comas por puntos
    val = val.replace(/,/g, '.');

    // remover caracteres no numéricos excepto el punto
    val = val.replace(/[^0-9.]/g, '');

    // permitir solo un punto decimal
    const firstDot = val.indexOf('.');
    if (firstDot !== -1) {
      val = val.slice(0, firstDot + 1) + val.slice(firstDot + 1).replace(/\./g, '');
    }

    input.value = val;

    // ajustar la posición del cursor después de la limpieza
    const newPos = Math.min(cursor, val.length);
    try { input.setSelectionRange(newPos, newPos); } catch (e) { /* ignore */ }
  }

  function formatoDecimal(value) {
    return Number(value).toFixed(2).toString().replace(',', '.');
  }

  function CambioUsd() {
    const usd = pasar_Decimal(usdEntrada.value);
    const tasa = pasar_Decimal(tasaEntrada.value);
    bsEntrada.value = tasa > 0 ? formatoDecimal(usd * tasa) : '';
  }

  function CambioBs() {
    const bs = pasar_Decimal(bsEntrada.value);
    const tasa = pasar_Decimal(tasaEntrada.value);
    usdEntrada.value = tasa > 0 ? formatoDecimal(bs / tasa) : '';
  }

  let campoEditado = null;

  usdEntrada?.addEventListener('input', () => {
    sanitizeNumericInput(usdEntrada);
    campoEditado = 'usd';
    CambioUsd();
  });

  bsEntrada?.addEventListener('input', () => {
    sanitizeNumericInput(bsEntrada);
    campoEditado = 'bs';
    CambioBs();
  });

  bsEntrada?.addEventListener('change', () => {
    sanitizeNumericInput(bsEntrada);
    campoEditado = 'bs';
    CambioBs();
  });

  tasaEntrada?.addEventListener('input', () => {
    sanitizeNumericInput(tasaEntrada);
    if (campoEditado === 'bs') {
      CambioBs();
    } else {
      CambioUsd();
    }
  });

  document.addEventListener('DOMContentLoaded', () => {
    if (usdEntrada) usdEntrada.value = '';
    if (bsEntrada) bsEntrada.value = '';
    campoEditado = null;
  });

