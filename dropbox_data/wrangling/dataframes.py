import pandas as pd
import logging
import os
from pathlib import Path
from dropbox_data.utils.date_extractor import extract_base_time
from dropbox_data.utils.numbers_formatters import format_numeric_columns
from dropbox_data.config import CSV_OUTPUT_PATH

logger = logging.getLogger(__name__)

def wrangle_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa o DataFrame:
    1. Extrai base_time da coluna post_extracted_datetime
    2. Para cada post_id, mantém todas as datas mas apenas o registro mais recente para outras colunas
    3. Formata colunas numéricas após ordenação
    
    Args:
        df (pd.DataFrame): DataFrame original
    
    Returns:
        pd.DataFrame: DataFrame processado
    """
    try:
        logger.info(f"Iniciando processamento de {len(df)} registros")
        
        # Primeiro, extraímos o base_time
        df = extract_base_time(df)
        logger.info("Base time extraído com sucesso")
        
        # Identificamos colunas de data
        date_columns = ['post_extracted_datetime', 'base_time']
        other_columns = [col for col in df.columns if col not in date_columns and col != 'post_id']
        
        # Criamos um DataFrame com todas as datas
        dates_df = df.groupby('post_id')[date_columns].agg(list).reset_index()
        logger.info("Datas agrupadas por post_id")
        
        # Para as outras colunas, pegamos o último registro de cada post_id
        latest_records = (df.sort_values('post_extracted_datetime')
                         .groupby('post_id', group_keys=False)[other_columns]
                         .last()
                         .reset_index())
        logger.info("Últimos registros extraídos para outras colunas")
        
        # Juntamos os dois DataFrames
        final_df = pd.merge(latest_records, dates_df, on='post_id', how='left')
        
        # Explodimos as listas de datas para criar registros individuais
        final_df = final_df.explode('post_extracted_datetime')
        final_df = final_df.explode('base_time')
        
        # Ordenamos por post_id e data
        final_df = final_df.sort_values(['post_id', 'post_extracted_datetime'])
        
        # Aplicamos a formatação numérica após a ordenação
        final_df = format_numeric_columns(final_df)
        logger.info("Colunas numéricas formatadas após ordenação")
        
        logger.info(f"Processamento concluído. Resultado final: {len(final_df)} registros")
        
        return final_df
        
    except Exception as e:
        logger.error(f"Erro ao processar DataFrame: {e}")
        raise

def process_csv_file(input_path: str, output_path: str, chunk_size: int = 100000):
    """
    Processa o arquivo CSV em chunks para evitar problemas de memória.
    
    Args:
        input_path (str): Caminho do arquivo de entrada
        output_path (str): Caminho do arquivo de saída
        chunk_size (int): Tamanho de cada chunk
    """
    try:
        # Garante que o diretório de saída existe
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Iniciando processamento do arquivo: {input_path}")
        logger.info(f"Arquivo será salvo em: {output_path}")
        
        # Lê os post_ids existentes se o arquivo de saída já existir
        existing_post_ids = set()
        if os.path.exists(output_path):
            existing_df = pd.read_csv(output_path, sep=';', usecols=['post_id'])
            existing_post_ids = set(existing_df['post_id'])
            logger.info(f"Encontrados {len(existing_post_ids)} post_ids existentes")
        
        # Lê o arquivo em chunks
        chunks = pd.read_csv(input_path, sep=';', chunksize=chunk_size)
        
        # Processa o primeiro chunk e salva com cabeçalho
        first_chunk = True
        total_records = 0
        
        for chunk in chunks:
            # Filtra apenas novos post_ids no chunk
            if existing_post_ids:
                chunk = chunk[~chunk['post_id'].isin(existing_post_ids)]
            
            if not chunk.empty:
                processed_chunk = wrangle_dataframe(chunk)
                
                # Salva o chunk processado
                processed_chunk.to_csv(
                    output_path,
                    mode='w' if first_chunk and not existing_post_ids else 'a',
                    header=first_chunk and not existing_post_ids,
                    index=False,
                    sep=';'
                )
                
                total_records += len(processed_chunk)
                first_chunk = False
                logger.info(f"Processados {total_records} registros até agora")
        
        logger.info(f"Processamento concluído. Total de registros: {total_records}")
        
        # Verifica se o arquivo foi realmente criado
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"Arquivo criado com sucesso. Tamanho: {file_size/1024/1024:.2f} MB")
        else:
            logger.error("Arquivo não foi criado!")
        
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {e}")
        raise

if __name__ == "__main__":
    try:
        # Configura logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Define caminhos dos arquivos
        input_file = CSV_OUTPUT_PATH
        output_file = str(Path(CSV_OUTPUT_PATH).parent / 'data_processed.csv')
        
        logger.info(f"Arquivo de entrada: {input_file}")
        logger.info(f"Arquivo de saída: {output_file}")
        
        # Processa o arquivo
        process_csv_file(input_file, output_file)
        
    except Exception as e:
        logger.error(f"Erro ao executar script: {e}")
        raise