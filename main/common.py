import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler
# ログの出力名を設定（1）
logger = logging.getLogger('arrest')

# ログレベルの設定（2）
logger.setLevel(logging.DEBUG)

# `RainbowLoggingHandler` を使う準備
handler = RainbowLoggingHandler(sys.stderr)
logger.addHandler(handler)

# ログのファイル出力先を設定（3）
fh = logging.FileHandler('../log/test.log')
logger.addHandler(fh)

# # ログのコンソール出力の設定（4）
# sh = logging.StreamHandler()
# logger.addHandler(sh)

# ログの出力形式の設定
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
# sh.setFormatter(formatter)
