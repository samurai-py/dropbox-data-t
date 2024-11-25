import os
import pandas as pd
from dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox_data.config import (
    PATH_DROPBOX, 
    CSV_DELIMITER, 
    CSV_OUTPUT_PATH, 
    TEMP_DOWNLOAD_PATH
)
import logging

logger = logging.getLogger(__name__)

class DropboxDownloader:
    def __init__(self, access_token=None):
        if not access_token:
            logger.error("Token de acesso não fornecido")
            raise ValueError("É necessário fornecer um token de acesso")
            
        self.dbx = Dropbox(access_token)
        self.data_path = CSV_OUTPUT_PATH
        self.temp_dir = TEMP_DOWNLOAD_PATH
        
        # Cria diretório temporário se não existir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def list_csv_files(self, dropbox_path):
        """Lista todos os arquivos CSV no caminho especificado do Dropbox"""
        try:
            files = self.dbx.files_list_folder(dropbox_path)
            return [entry.path_lower for entry in files.entries if entry.path_lower.endswith('.csv')]
        except ApiError as e:
            logger.error(f"Erro ao listar arquivos: {e}")
            return []

    def download_file(self, dropbox_path):
        """Baixa um arquivo do Dropbox"""
        local_path = os.path.join(self.temp_dir, os.path.basename(dropbox_path))
        try:
            with open(local_path, 'wb') as f:
                metadata, result = self.dbx.files_download(path=dropbox_path)
                f.write(result.content)
            return local_path
        except ApiError as e:
            logger.error(f"Erro ao baixar arquivo {dropbox_path}: {e}")
            return None

    def merge_files(self):
        """Concatena os arquivos baixados com o arquivo data.csv existente"""
        try:
            dfs = []  # Lista para armazenar DataFrames
            failed_files = []  # Lista para arquivos com erro
            
            # Se existe arquivo data.csv, lê primeiro
            if os.path.exists(self.data_path):
                try:
                    logger.info(f"Lendo arquivo existente: {self.data_path}")
                    existing_df = pd.read_csv(
                        self.data_path, 
                        sep=CSV_DELIMITER, 
                        encoding='utf-8-sig',
                        low_memory=False  # Evita o warning de dtype
                    )
                    dfs.append(existing_df)
                except Exception as e:
                    logger.error(f"Erro ao ler arquivo existente: {e}")

            # Lista todos os arquivos na pasta temporária
            temp_files = [os.path.join(self.temp_dir, f) for f in os.listdir(self.temp_dir) 
                         if f.endswith('.csv')]
            
            # Loop pelos arquivos CSV
            for file in temp_files:
                try:
                    logger.info(f"Processando arquivo: {file}")
                    df = pd.read_csv(
                        file, 
                        sep=CSV_DELIMITER, 
                        encoding='utf-8-sig',
                        low_memory=False
                    )
                    dfs.append(df)
                except Exception as e:
                    logger.error(f"Erro ao ler o arquivo {file}: {e}")
                    failed_files.append(file)

            # Concatenar todos os DataFrames se houver algum
            if dfs:
                combined_df = pd.concat(dfs, ignore_index=True)
                
                # Salvar o DataFrame combinado mantendo todos os registros
                combined_df.to_csv(
                    self.data_path, 
                    sep=CSV_DELIMITER, 
                    index=False, 
                    encoding='utf-8-sig'
                )
                logger.info(f"Arquivo salvo com sucesso: {len(combined_df)} registros")
            else:
                logger.warning("Nenhum arquivo foi processado com sucesso")

            if failed_files:
                logger.warning(f"Arquivos com erro: {failed_files}")

        except Exception as e:
            logger.error(f"Erro durante o merge de arquivos: {e}")
            raise

    def cleanup(self):
        """Remove os arquivos temporários"""
        try:
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            logger.info("Arquivos temporários removidos")
        except Exception as e:
            logger.error(f"Erro ao limpar arquivos temporários: {e}")

def extract_data(access_token=None, download_files=True):
    try:
        downloader = DropboxDownloader(access_token)
        
        if download_files:
            # Lista arquivos CSV no Dropbox
            dropbox_files = downloader.list_csv_files(PATH_DROPBOX)
            
            # Baixa cada arquivo
            for file_path in dropbox_files:
                downloader.download_file(file_path)
        
        # Mescla os arquivos
        downloader.merge_files()
        
        # Limpa arquivos temporários
        downloader.cleanup()
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        raise

if __name__ == "__main__":
    extract_data(download_files=False) 