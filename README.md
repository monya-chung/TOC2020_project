姓名: 鍾孟岳
學號: F74076182

TOC project 說明

1. 首先須在Line Bot 網站登錄建立developer
Line developers : https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2Fchannel%2Fnew%3Ftype%3Dmessaging-api

2. 開啟本機網站http 8000 的網路服務(利用ngrok)
ngrok http 8000

3. 取得服務網址後，需到Line developers 的Messaging API settings下，修改Webhook URL，參考如下:
https://ff0bead444a8.ngrok.io/webhook

4. 修改圖片資料取得的網址，參考如下:
"https://9d439982e52d.ngrok.io/my_travel_image/IMG_1.jpg"
(因本機網路服務太慢，建議由另外較快的電腦提供服務)

5. 開始執行本機網路服務(在TOC project目錄下)
python app.py

6. 利用手機的line app加入QR code即可開始聊天服務

7. project 設計內容說明
    (1)主題:分享過去旅遊經驗
    (2)menu選單(state 1)以2個案例分享，分別是->離島風光旅遊(state 2)、單車環島旅遊(state 3)，並可以選擇看FSM圖片(state 6)
    (3)在離島風光旅遊(state 2)可以選擇->看照片(state 4)、返回選單(state 1)
    (4)在單車環島旅遊(state 3)可以選擇->看照片(state 5)、返回選單(state 1)
    (5)看FSM圖片(state 6)後，只能輸入"0"返回menu選單(state 1)

8. 心得及遇到的問題
    本次project(聊天機器人)利用Line bot SDK的功能，體驗提供多種方便的服務，未來可以更加充實內容，或利用作為其他網路服務。
遇到的主要問題還是graphviz的module安裝問題，因為一直不成功，雖然助教有提供建議，但在時間緊迫因素下，只好自己寫一個狀態變化的function，
代替為graphviz module的簡易版功能(無法自動繪圖)，所以以另外可以執行graphviz的電腦跑繪圖功能，再儲存及上傳繪圖結果。
此外，在收集資料及研讀前人大作下也花了不少時間，真佩服前輩們。