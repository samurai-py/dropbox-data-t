import logging
from dropbox_data.config import LOG_PATH, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, filename=LOG_PATH)

logger = logging.getLogger(__name__)

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()