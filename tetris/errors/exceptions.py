class TetrisError(Exception):
    """專案內的基底例外類別。"""

class ConfigError(TetrisError):
    """設定檔格式或欄位不合法。"""

class SaveFileError(TetrisError):
    """讀寫檔案失敗（IO/權限/路徑等）。"""

class CorruptedDataError(TetrisError):
    """資料檔內容損毀或無法解析。"""

class InvalidMoveError(TetrisError):
    """不合法移動（碰撞或超出邊界）。"""
