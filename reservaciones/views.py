from django.shortcuts import render

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Evento, Sala

def eventos_json(request):
    eventos = Evento.objects.all()
    data = []
    for evento in eventos:
        data.append({
            "id": evento.id,
            "title": evento.nombre_evento,
            "start": evento.fecha_inicio.isoformat(),
            "end": evento.fecha_fin.isoformat(),
            "resourceIds": [sala.id for sala in evento.salas.all()],
            "color": evento.color,
        })
    return JsonResponse(data, safe=False)

def salas_json(request):
    salas = Sala.objects.all()
    data = []
    for sala in salas:
        data.append({
            "id": sala.id,
            "title": sala.nombre
        })
    return JsonResponse(data, safe=False)

from django.utils import timezone

def evento_detalle(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    inicio_local = timezone.localtime(evento.fecha_inicio)
    fin_local = timezone.localtime(evento.fecha_fin)
    
    data = {
        "title": evento.nombre_evento,
        "start": inicio_local.strftime('%d/%m/%Y %I:%M %p'),
        "end": fin_local.strftime('%d/%m/%Y %I:%M %p'),
        "start_iso": inicio_local.strftime('%Y-%m-%dT%H:%M'),
        "end_iso": fin_local.strftime('%Y-%m-%dT%H:%M'),
        "asistentes": evento.asistentes_esperados,
        "estado": evento.estado,
        "requerimientos": evento.requerimientos,
        "salas": [sala.id for sala in evento.salas.all()],
        "color": evento.color,
    }
    return JsonResponse(data)

def eventos_del_dia(request, fecha):
    eventos = Evento.objects.filter(fecha_inicio__date=fecha)
    data = []
    for evento in eventos:
        data.append({
            "id": evento.id,
            "nombre_evento": evento.nombre_evento
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def actualizar_evento(request, evento_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        evento = Evento.objects.get(id=evento_id)
        
        nueva_inicio = data['start']
        nueva_fin = data['end']
        salas_ids = [sala.id for sala in evento.salas.all()]

        conflictos = Evento.objects.filter(
            salas__id__in=salas_ids,
            fecha_inicio__lt=nueva_fin,
            fecha_fin__gt=nueva_inicio
        ).exclude(id=evento.id)

        if conflictos.exists():
            return JsonResponse({'status': 'error', 'mensaje': 'Hay un conflicto de horario con otra reservación'}, status=409)

        evento.fecha_inicio = nueva_inicio
        evento.fecha_fin = nueva_fin
        evento.color = data.get('color', evento.color)
        evento.save()
        return JsonResponse({'status': 'ok'})



# Views para cargar páginas

def agenda(request):
    eventos = Evento.objects.all()
    salas = Sala.objects.all()
    return render(request, 'reservaciones/calendario.html', {
        'eventos': eventos,
        'salas': salas,
    })