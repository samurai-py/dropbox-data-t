import os
import pandas as pd
from dropbox import Dropbox
from dropbox.exceptions import ApiError
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class DropboxDownloader:
    def __init__(self):
        self.dbx = Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))
        self.data_path = 'src/csv_files/data.csv'
        self.temp_dir = 'temp_downloads'
        
        # Cria diretório temporário se não existir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def list_csv_files(self, dropbox_path):
        """Lista todos os arquivos CSV no caminho especificado do Dropbox"""
        try:
            files = self.dbx.files_list_folder(dropbox_path)
            return [entry.path_lower for entry in files.entries if entry.path_lower.endswith('.csv')]
        except ApiError as e:
            print(f"Erro ao listar arquivos: {e}")
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
            print(f"Erro ao baixar arquivo {dropbox_path}: {e}")
            return None

    def merge_files(self):
        """Concatena os arquivos baixados com o arquivo data.csv existente"""
        # Lê o arquivo data.csv existente se houver
        if os.path.exists(self.data_path):
            existing_data = pd.read_csv(self.data_path)
            existing_post_ids = set(existing_data['post_id'])
        else:
            existing_data = pd.DataFrame()
            existing_post_ids = set()

        # Lista todos os arquivos na pasta temporária
        temp_files = [f for f in os.listdir(self.temp_dir) if f.endswith('.csv')]
        
        # Processa cada arquivo
        new_data = []
        for file in temp_files:
            df = pd.read_csv(os.path.join(self.temp_dir, file))
            
            # Filtra apenas registros com post_ids novos
            new_records = df[~df['post_id'].isin(existing_post_ids)]
            if not new_records.empty:
                new_data.append(new_records)

        # Concatena os novos dados
        if new_data:
            combined_new_data = pd.concat(new_data, ignore_index=True)
            final_data = pd.concat([existing_data, combined_new_data], ignore_index=True)
            
            # Salva o resultado
            final_data.to_csv(self.data_path, index=False)
            print(f"Adicionados {len(combined_new_data)} novos registros")
        else:
            print("Nenhum novo registro para adicionar")

    def cleanup(self):
        """Remove os arquivos temporários"""
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))

def main():
    downloader = DropboxDownloader()
    
    # Lista arquivos CSV no Dropbox
    dropbox_files = downloader.list_csv_files(PATH_DROPBOX)
    
    # Baixa cada arquivo
    for file_path in dropbox_files:
        downloader.download_file(file_path)
    
    # Mescla os arquivos
    downloader.merge_files()
    
    # Limpa arquivos temporários
    downloader.cleanup()

if __name__ == "__main__":
    main() 