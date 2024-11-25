from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox_data.config import DROPBOX_APP_KEY, DROPBOX_APP_SECRET

APP_KEY = DROPBOX_APP_KEY
APP_SECRET = DROPBOX_APP_SECRET

auth_flow = DropboxOAuth2FlowNoRedirect(
    APP_KEY,
    APP_SECRET,
    token_access_type='offline'
)

# 1. Obtém a URL de autorização
auth_url = auth_flow.start()
print("1. Acesse esta URL:", auth_url)
print("2. Clique em 'Allow' (autorizar)")
print("3. Copie o código de autorização")

# 4. Cole o código de autorização aqui
auth_code = input("Cole o código de autorização aqui: ").strip()

try:
    # 5. Troca o código pelo refresh token
    oauth_result = auth_flow.finish(auth_code)
    print("\nRefresh Token:", oauth_result.refresh_token)
    print("Access Token:", oauth_result.access_token)
    print("\nCopie o Refresh Token e coloque no seu arquivo .env")
    
except Exception as e:
    print('Erro:', str(e)) 