import logging
from dropbox_data.config import LOG_PATH, LOG_LEVEL
from dropbox_data.main import process_data

logging.basicConfig(level=LOG_LEVEL, filename=LOG_PATH)

logger = logging.getLogger(__name__)

def run_pipeline():
    """
    Função principal que inicia o pipeline de processamento.
    """
    try:
        logger.info("Iniciando pipeline de processamento")
        df = process_data()
        logger.info("Pipeline concluído com sucesso")
        return df
    except Exception as e:
        logger.error(f"Erro durante execução do pipeline: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()