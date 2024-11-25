import pandas as pd
import logging

logger = logging.getLogger(__name__)

def format_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formata colunas numéricas do DataFrame, convertendo strings formatadas para inteiros.
    """
    try:
        df = df.copy()
        
        numeric_columns = [
            'post_likes',
            'post_comments',
            'post_visualizations',
            'followers',
            'post_video_visualizations'
        ]
        
        for column in numeric_columns:
            if column in df.columns:
                logger.info(f"Processando coluna: {column}")
                
                # Remove pontos e textos extras, mantém apenas números
                df[column] = df[column].astype(str).str.replace('.', '').str.extract('(\d+)')[0]
                
                # Converte para int
                df[column] = df[column].astype('Int64')
                
                # Log das estatísticas
                non_null = df[column].count()
                total = len(df)
                logger.info(f"Coluna {column}: {non_null} valores válidos de {total} ({non_null/total*100:.2f}%)")
        
        return df
    
    except Exception as e:
        logger.error(f"Erro ao formatar colunas numéricas: {e}")
        raise

if __name__ == "__main__":
    # Configuração de logging para teste
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Teste com alguns valores
    test_df = pd.DataFrame({
        'post_likes': ['1.234', '2,5 mil', '3M', '4k', '5\n mil', 'abc'],
        'post_comments': ['123', '456 comentários', '1,5k comentários', 'sem comentários', '2.345'],
    })
    
    result = format_numeric_columns(test_df)
    print("\nResultados do teste:")
    print(result)
