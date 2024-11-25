# Dropbox Data Merger

Ferramenta automatizada para download, merge e processamento de arquivos CSV do Dropbox. A aplicação gerencia autenticação, download seletivo de arquivos novos/modificados e processamento em chunks para lidar com grandes volumes de dados.

## Características

- Autenticação automática com o Dropbox usando refresh tokens
- Download seletivo de arquivos novos ou modificados
- Processamento em chunks para eficiência de memória
- Extração e formatação de datas
- Conversão automática de campos numéricos
- Sistema de logging detalhado
- Tratamento de duplicatas

## Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd dropbox-data-merger
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -e .
```

## Configuração

1. Crie um aplicativo no [Dropbox App Console](https://www.dropbox.com/developers/apps):
   - Escolha "Scoped access"
   - Selecione "Full Dropbox" access
   - Em "Permissions", habilite:
     - files.metadata.read
     - files.content.read

2. Gere um refresh token usando o script fornecido:
```bash
python scripts/get_refresh_token.py
```

3. Crie um arquivo `.env` na raiz do projeto:
```env
PATH_DROPBOX="/seu/caminho/no/dropbox"
DROPBOX_APP_KEY="sua_app_key"
DROPBOX_APP_SECRET="seu_app_secret"
DROPBOX_REFRESH_TOKEN="seu_refresh_token"
LOG_LEVEL="INFO"
CSV_DELIMITER=";"
```

## Estrutura do Projeto

```
dropbox-data-merger/
├── dropbox_data/
│   ├── auth/               # Autenticação Dropbox
│   ├── extract/            # Download e merge de arquivos
│   ├── wrangling/          # Processamento de dados
│   ├── utils/              # Funções utilitárias
│   ├── config.py          # Configurações
│   └── main.py            # Ponto de entrada
├── scripts/
│   └── get_refresh_token.py
├── logs/                   # Arquivos de log
└── src/
    ├── csv_files/         # Arquivos CSV processados
    └── temp_downloads/    # Downloads temporários
```

## Uso

### Como Módulo Python

```python
from dropbox_data import run_pipeline

# Executa o pipeline completo
result = run_pipeline()
```

### Como Script

```bash
start_app
```

## Pipeline de Processamento

1. **Autenticação**
   - Verifica token existente
   - Renova automaticamente se necessário

2. **Extração**
   - Lista arquivos no Dropbox
   - Identifica arquivos novos/modificados
   - Download seletivo
   - Merge inicial dos arquivos

3. **Processamento**
   - Extração de datas base
   - Formatação de campos numéricos
   - Processamento em chunks
   - Remoção de duplicatas por post_id

4. **Salvamento**
   - Arquivo final em src/csv_files/final_data.csv
   - Mantém histórico de processamento

## Logs

A aplicação mantém logs detalhados em `copilot_marketing.log`, incluindo:
- Informações de autenticação
- Status de downloads
- Estatísticas de processamento
- Erros e avisos

## Manutenção

- Os arquivos temporários são limpos automaticamente
- Tokens são renovados automaticamente
- O histórico de arquivos processados é mantido em `processed_files.txt`

## Requisitos

- Python 3.8+
- Dropbox API v2
- Pandas
- Python-decouple

## Tratamento de Erros

A aplicação inclui tratamento robusto de erros para:
- Falhas de autenticação
- Problemas de conexão
- Erros de processamento
- Problemas de formato de arquivo

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Crie um Pull Request

## Licença

[Sua licença aqui]