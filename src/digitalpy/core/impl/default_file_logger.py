import logging
import logging.config
from digitalpy.core.logger import Logger
import pathlib
import os


class DefaultFileLogger(Logger):

    base_logging_path = "FTSLogs/"

    log_level = logging.DEBUG

    log_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", "%m-%d-%Y %H:%M:%S"
    )

    def __init__(self, name, config_file=""):

        self.config_file = config_file

        if not os.path.exists(pathlib.Path(DefaultFileLogger.base_logging_path, name)):
            os.mkdir(pathlib.Path(DefaultFileLogger.base_logging_path, name))

        self.logger = self.get_new_logger(name, config_file)

    @staticmethod
    def set_log_level(level):
        DefaultFileLogger.log_level = level

    @staticmethod
    def set_base_logging_path(path):
        DefaultFileLogger.base_logging_path = path

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def fatal(self, message):
        self.logger.fatal(message)

    def create_logger_instance(
        self, name, config_file, formatter, log_level, logging_path
    ):
        logging.config.fileConfig(config_file)

        logger = logging.getLogger(name)

        logger.setLevel(log_level)

        handler = logging.FileHandler(logging_path)
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger

    def get_new_logger(self, name, config_file=None):

        return self.create_logger_instance(
            name,
            config_file,
            DefaultFileLogger.log_formatter,
            DefaultFileLogger.log_level,
            pathlib.Path(
                DefaultFileLogger.base_logging_path,
                name,
                f"{logging.getLevelName(DefaultFileLogger.log_level)}.log",
            ),
        )

    def get_logger(self):
        return self.logger
