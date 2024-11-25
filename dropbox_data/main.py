import logging
from pathlib import Path
from dropbox_data.wrangling.dataframes import process_csv_file
from dropbox_data.extract.dropbox_download import DropboxDownloader
from dropbox_data.config import CSV_OUTPUT_PATH, PATH_DROPBOX

logger = logging.getLogger(__name__)

def download_and_merge():
    """
    Baixa arquivos do Dropbox e faz o merge inicial.
    """
    try:
        logger.info("Iniciando download e merge dos arquivos do Dropbox")
        downloader = DropboxDownloader()
        
        # Lista e baixa arquivos do Dropbox
        dropbox_files = downloader.list_csv_files(PATH_DROPBOX)
        for file_path in dropbox_files:
            downloader.download_file(file_path)
        
        # Faz o merge dos arquivos baixados
        downloader.merge_files()
        
        # Limpa arquivos temporários
        downloader.cleanup()
        
        logger.info("Download e merge concluídos com sucesso")
        
    except Exception as e:
        logger.error(f"Erro durante download e merge: {e}")
        raise

def process_data(chunk_size: int = 100000):
    """
    Função principal que orquestra o processamento dos dados.
    """
    try:
        # Primeiro faz o download e merge dos arquivos do Dropbox
        download_and_merge()
        
        # Define caminhos
        base_file = Path('src/csv_files/final_data.csv')
        new_data_file = Path(CSV_OUTPUT_PATH)
        
        # Processa o arquivo usando process_csv_file
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
