from django.urls import path
from .views import generate_invoice, enviar_correo

urlpatterns = [
    path('invoice/', generate_invoice, name='generate_invoice'),
        path('send_correo', enviar_correo, name='sendCorreo'),

]
