import logging
import os
import sys

from datetime import datetime


def setupLogger(log_file="app.log"):
    log_folder = "logging"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_path = os.path.join(log_folder, log_file)

    # Очищаем старый лог-файл
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"Log started at {datetime.now()}\n")

    # Настраиваем логгер
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Очищаем существующие обработчики
    logger.handlers.clear()

    # Создаем новые обработчики
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    console_handler = logging.StreamHandler(sys.stdout)

    # Устанавливаем формат для обработчиков
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Создаем логгер только один раз
logger = setupLogger()
