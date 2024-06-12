import logging
import datetime

def setup_logging(log_filename='log.txt'):
    """
    配置日志记录系统。
    :param log_filename: 日志文件的名称。
    """
    # 定义日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    # 创建日志文件处理器
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))

    # 创建或获取日志器，并设置日志级别
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger

def log_info(logger, message):
    """
    记录一条INFO级别的日志。
    :param logger: 日志器对象。
    :param message: 要记录的消息。
    """
    logger.info(f" {datetime.datetime.now()} - {message}")

def log_error(logger, message):
    """
    记录一条ERROR级别的日志。
    :param logger: 日志器对象。
    :param message: 要记录的消息。
    """
    logger.error(f" {datetime.datetime.now()} - {message}")

# 示例用法：
# logger = setup_logging()
# log_info(logger, "这是一条信息级别的日志")
# log_error(logger, "这是一条错误级别的日志")