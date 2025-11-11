"""
URL configuration for softproject_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse
import os

def serve_frontend(request, path=''):
    """Serve frontend files"""
    frontend_dir = os.path.join(settings.BASE_DIR, 'frontend')
    
    if not path or path == 'index.html':
        file_path = os.path.join(frontend_dir, 'index.html')
    else:
        file_path = os.path.join(frontend_dir, path)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(open(file_path, 'rb'))
    
    # Default to index.html for SPA routing
    return FileResponse(open(os.path.join(frontend_dir, 'index.html'), 'rb'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # Serve frontend files
    path('', serve_frontend, name='frontend-index'),
    path('<path:path>', serve_frontend, name='frontend-files'),
]

