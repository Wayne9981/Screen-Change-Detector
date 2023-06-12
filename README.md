# Install
```zsh
pip install -r requirements.txt
```
建議安裝在虛擬環境上，python 版本 >= 3.9

# Usage
```zsh
python main.py
```
執行後 macOs 需要監控鍵盤輸入&執行腳本權限，在設定 &rarr; 隱私權與安全性 &rarr; 輸入監控／輔助使用 &rarr; 授予執行的應用程式權限，才能正常執行。

有可能出現 pyscreeze 執行錯誤，解決方案請參見 Question

預設按 z 能夠將當前畫面存入記憶體，再按能觸發比對功能，如果畫面有明顯變化，則創造一個 images 資料夾，並以發生時間作為檔名，將變化後的圖片存入資料夾。

按 esc 能跳出程式

確定設定無誤後，按 y 正式開始執行腳本，每 5 ~ 7 秒對螢幕畫面進行一次比對，持續不斷直到在 zsh 使用 ctrl + c 終止整支程式為止。

注意這時使用 esc 無法跳出程式

# Setting

## main.py:

logging.basicConfig 可以設定 level 為 INFO / DEBUG

INFO 的訊息比較少，但也比較簡潔

KeyboardEventHandler.handler 可以調整觸發腳本的按鍵與對應觸發功能

## callback.py

IMAGE_FOLDER: 存放截圖的資料夾。

DIFF_THRESHOLD: 0~1之間的數字，用來判斷差異多大時該存下圖片，數字越小代表閾值越低、越容易觸發截圖。

TIME_INTERVAL_SEC: 每次檢查螢幕之間的時間間隔，單位為秒。

## Question
https://github.com/asweigart/pyscreeze/pull/96
