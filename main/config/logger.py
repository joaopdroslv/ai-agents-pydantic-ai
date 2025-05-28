# my_logger.py
import logging
import os

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "info.log")

logger = logging.getLogger("my_project")  # nome fixo e único do logger
logger.setLevel(logging.INFO)

# Evita adicionar handlers duplicados
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = (
        False  # evita log duplicado no stdout (se root logger também imprimir)
    )
