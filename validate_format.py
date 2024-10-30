import re
from openai import OpenAI, OpenAIError

# 檢查電子郵件格式，確保包含 "@" 和域名
def validate_email_format(data: dict) -> bool:
    if 'email' in data:
        email = data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print(f"Invalid email format detected: {email}")
            return False
    return True