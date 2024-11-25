import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_base_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrai o datetime mais antigo para cada post_id da coluna post_extracted_datetime.
    
    Args:
        df (pd.DataFrame): DataFrame contendo as colunas 'post_id' e 'post_extracted_datetime'
        
    Returns:
        pd.DataFrame: DataFrame original com a nova coluna 'base_time'
    """
    try:
        # Cria uma cópia do DataFrame para não modificar o original
        df = df.copy()
        
        # Especifica o formato da data explicitamente
        df['post_extracted_datetime'] = pd.to_datetime(
            df['post_extracted_datetime'], 
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        logger.info("Coluna post_extracted_datetime convertida para datetime")
        
        # Agrupa por post_id e pega o datetime mais antigo
        base_times = df.groupby('post_id')['post_extracted_datetime'].min()
        
        # Adiciona a nova coluna base_time
        df['base_time'] = df['post_id'].map(base_times)
        
        # Log das estatísticas
        total_posts = len(df['post_id'].unique())
        posts_with_time = base_times.notna().sum()
        logger.info(f"Base times extraídos para {posts_with_time} de {total_posts} posts")
        
        return df
    
    except Exception as e:
        logger.error(f"Erro ao extrair base_time: {e}")
        raise

if __name__ == "__main__":
    try:
        # Configura logging
        logging.basicConfig(level=logging.INFO)
        
        # Lê o DataFrame
        df = pd.read_csv('src/csv_files/data.csv', sep=';')
        
        # Extrai base_time
        df = extract_base_time(df)
        
        # Salva o resultado
        df.to_csv('src/csv_files/data_with_base_time.csv', sep=';', index=False)
        logger.info("Processamento concluído com sucesso")
        
    except Exception as e:
        logger.error(f"Erro durante o processamento: {e}")