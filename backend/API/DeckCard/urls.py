"""
URL configuration for DeckCard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404

# Redirección de la URL base al admin
def redirect_to_admin(request):
    return redirect('admin:index')

# Vista para manejar 404
def handle_404(request, exception=None):
    # Explícitamente lanzamos 404 para que Django use nuestro template personalizado
    raise Http404("Página no encontrada")

urlpatterns = [
    # Redirigir la raíz al admin
    path('', redirect_to_admin, name='index'),
    
    # Admin en su URL original (accesible tanto desde / como desde /admin/)
    path('admin/', admin.site.urls),
    
    # API de cartas
    path('api/', include('cards.urls')),
    
    # Captura cualquier otra URL y devuelve 404
    re_path(r'^.*$', handle_404),
]

# Asignar nuestro manejador de error 404 personalizado
handler404 = 'DeckCard.urls.handle_404'
