import logging
from logging import Logger


logger = logging.getLogger("logger")  # logger名loggerを取得
logger.setLevel(logging.DEBUG)  # loggerとしてはDEBUGで

# handler1: 標準出力
handler1 = logging.StreamHandler()
handler1.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)8s %(message)s"))

# handler2を作成: ファイル出力
handler2 = logging.FileHandler(filename="test.log")  # handler2はファイル出力
# handler2.setLevel(logging.WARN)  # handler2はLevel.WARN以上
handler2.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)8s %(message)s"))

# loggerに2つのハンドラを設定
logger.addHandler(handler1)
logger.addHandler(handler2)



def get_logger(name: str|None = None) -> Logger:
    return logger
