from decouple import config

# Debug variables
DEBUG: bool = config("DEBUG", default=False, cast=bool)
DEBUG_ID: str = config("DEBUG_ID", default="", cast=str)

CSV_DELIMITER: str = config("CSV_DELIMITER", default=";", cast=str)
CSV_OUTPUT_PATH: str = config("CSV_OUTPUT_PATH", cast=str, default="src/csv_files/data.csv")
TEMP_DOWNLOAD_PATH: str = config("TEMP_DOWNLOAD_PATH", cast=str, default="src/temp_downloads")

# External API variables
DROPBOX_APP_KEY: str = config("DROPBOX_APP_KEY", cast=str)
DROPBOX_APP_SECRET: str = config("DROPBOX_APP_SECRET", cast=str)
DROPBOX_REFRESH_TOKEN: str = config("DROPBOX_REFRESH_TOKEN", cast=str)
PATH_DROPBOX: str = config("PATH_DROPBOX", cast=str)

# Logging configuration
LOG_LEVEL: str = config("LOG_LEVEL", default="INFO", cast=str)
LOG_PATH: str = config("LOG_PATH", default="copilot_marketing.log", cast=str)
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s|%(levelname)s|%(name)s|%(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        }
    },
    "handlers": {
        "default": {
            "level": LOG_LEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": LOG_LEVEL,
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": LOG_PATH,
        },
    },
    "loggers": {
        "": {"handlers": ["default", "file"], "level": LOG_LEVEL, "propagate": True},
    },
}
