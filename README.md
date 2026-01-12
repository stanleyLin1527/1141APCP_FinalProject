# Tetris Project (Python + Pygame)

## 安裝
```bash
pip install -r requirements.txt
```

## 執行
```bash
python main.py
```

## 操作
- 左/右：移動
- 上：旋轉
- 下：軟降（加速下落）
- Space：硬降（Hard drop）
- C：Hold（暫存/交換方塊；一個落下週期只能用一次，直到方塊鎖定才解鎖）
- P：暫停
- R：重新開始（Game Over 畫面）
- ESC：返回主選單 / 退出

## 資料檔
- `data/settings.json`：按鍵/音量/玩家名稱等設定
- `data/highscores.json`：排行榜（前 10 名）
