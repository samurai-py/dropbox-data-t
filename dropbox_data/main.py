import logging
from pathlib import Path
from dropbox import files
from dropbox_data.wrangling.dataframes import process_csv_file
from dropbox_data.extract.dropbox_download import extract_data
from dropbox_data.config import CSV_OUTPUT_PATH, PATH_DROPBOX
from dropbox_data.auth import DropboxAuthManager

logger = logging.getLogger(__name__)

def check_for_updates(downloader):
    """
    Verifica se há novos arquivos ou modificações no Dropbox.
    """
    try:
        # Carrega registro de arquivos já processados
        processed_files = Path('src/csv_files/processed_files.txt')
        if processed_files.exists():
            with open(processed_files, 'r') as f:
                processed = {line.strip().split(',')[0]: line.strip().split(',')[1] 
                           for line in f.readlines()}
        else:
            processed = {}
            
        # Lista arquivos do Dropbox
        dropbox_files = downloader.dbx.files_list_folder(PATH_DROPBOX)
        
        new_or_modified = []
        for entry in dropbox_files.entries:
            if isinstance(entry, files.FileMetadata):
                # Verifica se arquivo é novo ou foi modificado
                if (entry.path_lower not in processed or 
                    processed[entry.path_lower] != entry.rev):
                    new_or_modified.append(entry.path_lower)
        
        return new_or_modified
        
    except Exception as e:
        logger.error(f"Erro ao verificar atualizações: {e}")
        raise

def update_processed_files(downloader, processed_files):
    """
    Atualiza o registro de arquivos processados.
    """
    try:
        # Lista arquivos atuais do Dropbox
        dropbox_files = downloader.dbx.files_list_folder(PATH_DROPBOX)
        
        # Atualiza registro
        with open('src/csv_files/processed_files.txt', 'w') as f:
            for entry in dropbox_files.entries:
                if isinstance(entry, files.FileMetadata):
                    f.write(f"{entry.path_lower},{entry.rev}\n")
                    
    except Exception as e:
        logger.error(f"Erro ao atualizar registro de arquivos: {e}")
        raise

def download_and_merge(downloader, files_to_process):
    """
    Baixa apenas arquivos novos ou modificados do Dropbox e faz o merge.
    """
    try:
        if not files_to_process:
            logger.info("Nenhum arquivo novo ou modificado encontrado")
            return False
            
        logger.info(f"Baixando {len(files_to_process)} arquivos novos/modificados")
        
        # Baixa apenas os arquivos necessários
        for file_path in files_to_process:
            downloader.download_file(file_path)
        
        # Faz o merge dos arquivos baixados
        downloader.merge_files()
        
        # Limpa arquivos temporários
        downloader.cleanup()
        
        # Atualiza registro de arquivos processados
        update_processed_files(downloader, files_to_process)
        
        logger.info("Download e merge concluídos com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro durante download e merge: {e}")
        raise

def process_data(chunk_size: int = 100000):
    """
    Função principal que orquestra o processamento dos dados.
    """
    try:
        # Inicializa autenticação
        logger.info("Iniciando processo de autenticação")
        auth_manager = DropboxAuthManager()
        access_token = auth_manager.get_valid_access_token()
        
        if not access_token:
            logger.error("Token não obtido. Verifique as credenciais no arquivo .env")
            raise Exception("Não foi possível obter um token válido")
        
        # Extrai dados usando o token válido
        extract_data(access_token=access_token)
        
        # Define caminhos
        base_file = Path('src/csv_files/final_data.csv')
        new_data_file = Path(CSV_OUTPUT_PATH)
        
        # Processa o arquivo
        process_csv_file(
            input_path=str(new_data_file),
            output_path=str(base_file),
            chunk_size=chunk_size
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Erro durante o processamento: {e}")
        raise

if __name__ == "__main__":
    process_data()
