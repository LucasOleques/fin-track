"""
WSGI config for fin_track_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
import logging
from pathlib import Path

# Adicionar o caminho do projeto ao sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR.parent))

from django.core.wsgi import get_wsgi_application
from django.middleware.security import SecurityMiddleware

# Configurar o módulo de settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fin_track_project.settings')

# Configurar logging
logger = logging.getLogger(__name__)

# Inicializar aplicação Django
try:
    application = get_wsgi_application()
    
    # Adicionar middleware de segurança para produção
    if os.environ.get('DEBUG') == 'False':
        application = SecurityMiddleware(application, hsts_seconds=31536000)
    
    logger.info("WSGI Application inicializada com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar WSGI Application: {str(e)}")
    raise