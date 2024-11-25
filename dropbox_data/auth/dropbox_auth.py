import json
from datetime import datetime, timedelta
from dropbox_data.config import DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN
from dropbox import Dropbox
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DropboxAuthManager:
    def __init__(self):
        self.app_key = DROPBOX_APP_KEY
        self.app_secret = DROPBOX_APP_SECRET
        self.refresh_token = DROPBOX_REFRESH_TOKEN
        
        logger.info("Credenciais carregadas:")
        logger.info(f"App Key presente: {'Sim' if self.app_key else 'Não'}")
        logger.info(f"App Secret presente: {'Sim' if self.app_secret else 'Não'}")
        logger.info(f"Refresh Token presente: {'Sim' if self.refresh_token else 'Não'}")
        
        self.token_file = Path('dropbox_data/auth/token.json')
        self.token_file.parent.mkdir(parents=True, exist_ok=True)

    def refresh_access_token(self):
        """Atualiza o token usando o refresh_token"""
        try:
            logger.info(f"Tentando atualizar token com app_key: {self.app_key[:5]}...")
            logger.info(f"Refresh token presente: {bool(self.refresh_token)}")
            
            # Cria um cliente Dropbox com as credenciais
            dbx = Dropbox(
                oauth2_refresh_token=self.refresh_token,
                app_key=self.app_key,
                app_secret=self.app_secret
            )
            
            # Testa a conexão para garantir que o token é válido
            dbx.check_user()
            
            # Se chegou aqui, o token é válido
            token_data = {
                'access_token': dbx._oauth2_access_token,
                'expires_at': (datetime.now() + timedelta(hours=4)).isoformat()
            }
            
            # Salva o token
            with open(self.token_file, 'w') as f:
                json.dump(token_data, f)
            
            logger.info("Access token refreshed successfully")
            return dbx._oauth2_access_token
            
        except Exception as e:
            logger.error(f"Error refreshing access token: {str(e)}")
            logger.error("Verifique se as credenciais no .env estão corretas")
            return None

    def get_valid_access_token(self):
        """Obtém um token de acesso válido"""
        try:
            # Tenta carregar token existente
            if self.token_file.exists():
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    
                # Verifica se o token ainda é válido
                expires_at = datetime.fromisoformat(token_data['expires_at'])
                if datetime.now() + timedelta(hours=1) < expires_at:
                    logger.info("Using existing valid token")
                    return token_data['access_token']
            
            # Se não tem token ou está expirado, gera novo
            logger.info("Token expired or not found, refreshing...")
            return self.refresh_access_token()
            
        except Exception as e:
            logger.error(f"Error getting valid access token: {e}")
            return None 