# JSON Extractor Using GPT

OpenAI API 在 2024/8 推出支援 [JSON 格式的輸出](https://openai.com/index/introducing-structured-outputs-in-the-api/)，所以此專案就是來實作 OpenAI GPT-4o (`gpt-4o-2024-08-06`) 模型，自動從使用者的輸入中提取姓名、電子郵件和電話號碼等資訊。使用了 `Streamlit` 作為前端框架，並提供了 `JSON Schema` 和 `Function Calling` 兩種提取資料的方法。

# 主要功能
- **資料提取模式**：支援 `JSON Schema` 和 `Function Calling` 兩種模式。
- **格式驗證**：自動驗證電子郵件格式，確保回傳資料的準確性。
- **歷史記錄**：儲存使用者輸入和 GPT 的回應，方便查看對話歷史。
- **資料保存**：成功提取的資料會以 JSON 格式保存至本地檔案。

# 使用方法
進入 [JSON Extractor]()。

## 輸入 OPENAI API 金鑰
輸入你的 OpenAI API 金鑰，點擊鍵盤「Enter」，即可開始使用。

## 輸入資料
選擇「JSON Schema」或「Function Calling」模式。在輸入框中輸入資料(參考格式如下)，接著點擊「Submit」按鈕，即可查看所提取的資料。
```
我的名字是Stella，請用 stelladai1028@gmail.com 聯絡我，電話是0988999999
```
```
Stella stelladai1028@gmail.com 0988999999
```
