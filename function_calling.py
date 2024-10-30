from openai import OpenAI, OpenAIError
from pydantic import ValidationError
from models import UserData
from typing import Optional, Union
import json
from validate_format import validate_email_format

def function_calling_response(user_input: str, memory: list, api_key: str) -> Union[Optional[UserData], str]:
    """
    使用 OpenAI 的 Function Calling 方法提取使用者資料。

    參數:
        user_input (str): 使用者輸入的文字。
        memory (list): 對話記憶，用於存儲對話歷史。
        api_key (str): OpenAI API 金鑰。

    返回:
        Optional[UserData]: 如果成功提取資料，返回 UserData 實例；否則返回錯誤訊息。
    """
    client = OpenAI(api_key=api_key)
    try:
        # 建立 OpenAI API 的請求，設置模型和調用參數
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0,
            # 定義tools
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "extract_user_data",
                        "description": "提取姓名、電子郵件和電話號碼。",
                        "strict": True,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "使用者的姓名"},
                                "email": {"type": "string", "description": "使用者的電子郵件"},
                                "phone": {"type": "string", "description": "使用者的電話號碼"}
                            },
                            "required": ["name", "email", "phone"],
                            "additionalProperties": False
                        }
                    }
                }
            ],
        )

        # 獲取 API 回應中的訊息
        message = response.choices[0].message
        print("Function Calling Response:", message.tool_calls)

        # 檢查是否調用函數
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments) # 將結果轉換為字典格式

            # 驗證電子郵件格式，若無效則返回錯誤訊息
            if not validate_email_format(arguments):
                return "Email format validation failed."

            if isinstance(arguments, dict):
                try:
                    # 將結果轉換為 UserData 實例
                    user_data = UserData(**arguments)
                    # 將LLM回應添加到對話歷史
                    memory.append({"role": "assistant", "content": arguments})
                    return user_data
                except ValidationError as ve:
                    print(f"JSON 解析錯誤: {ve}")
                    print(f"Arguments received: {arguments}")
                    return "Unable to extract valid data. Please check the input format."
        
        # 直接回應內容
        elif message.content:
            try:
                response_data = json.loads(message.content) # 將回應內容轉換為字典
                # 驗證電子郵件格式
                if validate_email_format(response_data):
                    # 將結果轉換為 UserData 實例
                    user_data = UserData(**response_data)
                    # 將LLM回應添加到對話歷史
                    memory.append({"role": "assistant", "content": response_data})
                    return user_data
                else:
                    return "Email format validation failed."
            except ValidationError as ve:
                print(f"JSON 解析錯誤: {ve}")
                print(f"Content received: {message.content}")
                return "Unable to extract valid data. Please check the input format."
        else:
            print("No function_call or content in the response message.")
            return "No function_call or content in the response message."

    except OpenAIError as e:
        print(f"OpenAI API 錯誤: {e}")
        return "OpenAI API error occurred. Please try again later."
