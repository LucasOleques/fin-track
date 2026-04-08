"""
ASGI config for fin_track_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import sys
import logging
from pathlib import Path

from django.core.asgi import get_asgi_application
from django.middleware.security import SecurityMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fin_track_project.settings')

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

try:
    application = get_asgi_application()
    
    if os.environ.get('DEBUG', 'True') == 'False':
        application = SecurityMiddleware(application, hsts_seconds=31536000)
        logger.info("SecurityMiddleware aplicado ao ASGI")
    
    logger.info("ASGI Application inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar ASGI: {str(e)}")
    raise
