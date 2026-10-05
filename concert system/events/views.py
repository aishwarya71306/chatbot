import json
from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Event


def event_payload(event):
    return {
        'day': event.date.strftime('%d'),
        'month': event.date.strftime('%b').upper(),
        'name': event.name,
        'details': event.details,
        'status': event.status,
        'statusText': event.get_status_display(),
        'sold': f'{event.tickets_sold:,}',
        'capacity': f'{event.capacity:,}' if event.capacity else '—',
    }


def seed_events():
    if Event.objects.exists():
        return
    Event.objects.bulk_create([
        Event(name='Northside Festival', details='Various artists · Riverside Park', date=date(2026, 8, 28), status='live', tickets_sold=2840, capacity=3500),
        Event(name='Luna Park Sessions', details='The Marías · Luna Park', date=date(2026, 9, 2), status='upcoming', tickets_sold=1240, capacity=2000),
        Event(name='Afterglow Tour', details='Juno Ray · The Forum', date=date(2026, 9, 14), status='sold', tickets_sold=1800, capacity=1800),
        Event(name='Electric Bloom', details='Maya Sol · The Glasshouse', date=date(2026, 9, 21), status='upcoming', tickets_sold=612, capacity=1200),
    ])


@csrf_exempt
def event_list(request):
    if request.method == 'GET':
        seed_events()
        return JsonResponse([event_payload(event) for event in Event.objects.all()], safe=False)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = Event.objects.create(
                name=data['name'],
                details=data['details'],
                date=data['date'],
                capacity=data.get('capacity', 0),
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            return JsonResponse({'error': f'Invalid event data: {error}'}, status=400)
        return JsonResponse(event_payload(event), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
