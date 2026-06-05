from django.shortcuts import render
from .forms import ReportePagosForm

def gestion_reportes(request):
    ## agg la logica para generar el reporte de los ingresos/pagos
    form = ReportePagosForm(request.POST or None)
    return render(request, 'gestion_reportes.html', {'form': form})
