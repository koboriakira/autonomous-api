import logging
from logging import Logger
import os
import pathlib

logger = logging.getLogger("logger")  # logger名loggerを取得
if os.getenv("IS_DEV") == "local":
    PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

    logger.setLevel(logging.DEBUG)  # loggerとしてはDEBUGで

    # handler1: 標準出力
    handler1 = logging.StreamHandler()
    handler1.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)8s %(message)s"))

    # handler2を作成: ファイル出力
    log_file_path = f'%s/test.log' % PROJECT_ROOT_PATH
    print(log_file_path)
    if not os.path.exists(log_file_path):
        pathlib.Path(log_file_path).touch()
    handler2 = logging.FileHandler(filename=log_file_path)  # handler2はファイル出力
    handler2.setLevel(logging.INFO)  # handler2はLevel.ERROR以上
    handler2.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)8s %(message)s"))

    # loggerに2つのハンドラを設定
    logger.addHandler(handler1)
    logger.addHandler(handler2)


def get_logger(name: str|None = None) -> Logger:
    return logger
