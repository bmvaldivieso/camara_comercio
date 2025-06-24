# apps/backend/backend/views.py

from django.http import JsonResponse
from django.views import View

class TestConnectionView(View):
    def get(self, request):
        response = JsonResponse({'message': 'Conexión a Django exitosa desde Astro'})
        response['Content-Type'] = 'application/json; charset=utf-8'
        return response


