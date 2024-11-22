# Dropbox Data Merger

Ferramenta para download e merge de arquivos CSV do Dropbox.

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows
   ```
3. Instale o pacote:
   ```bash
   pip install -e .
   ```

## Configuração

1. Copie o arquivo `settings.ini` e configure suas variáveis:
   ```bash
   cp settings.ini.example settings.ini
   ```
2. Edite o arquivo `settings.ini` com suas configurações

## Uso

Execute o script principal: 