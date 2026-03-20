import logging
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(CURRENT_DIR, 'audit_trail.log')

# Configuração do Logger
logger = logging.getLogger('FinTrackAudit')
logger.setLevel(logging.INFO)

# Evita adicionar múltiplos handlers se o módulo for importado várias vezes
if not logger.handlers:
    # Cria o handler para escrever no arquivo
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    
    # Formato: DATA | USUÁRIO | AÇÃO | DETALHES
    formatter = logging.Formatter(
         'DATA: %(asctime)s \nUSUÁRIO: %(user_identifier)s \nAÇÃO: %(action_name)s \nDETALHES: %(details)s \n=======================================\n',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def registrar_log(user, action, details):
    """
    Registra uma alteração ou ação do sistema no arquivo de log.
    
    Args:
        user: Objeto User do Django ou string identificando o usuário.
        action (str): O que foi feito (ex: "Atualizar Perfil", "Excluir Transação").
        details (str): Detalhes específicos do que mudou.
    """
    # Tenta extrair informações legíveis do usuário
    user_identifier = str(user)
    if hasattr(user, 'email') and user.email:
        user_identifier = f"{user.get_full_name()} ({user.email})"
    elif hasattr(user, 'username'):
        user_identifier = user.username

    extra_data = {
        'user_identifier': user_identifier,
        'action_name': action,
        'details': details
    }
    
    logger.info(f"{action} executada.", extra=extra_data)