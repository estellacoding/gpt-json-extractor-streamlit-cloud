# app.py

import streamlit as st
from json_schema import json_schema_response
from function_calling import function_calling_response
from models import UserData

# 設定頁面標題和結構
st.set_page_config(page_title="JSON Extractor", layout="wide")

# 初始化會話狀態
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = "JSON Schema"

# API 金鑰輸入
st.sidebar.title("API Settings")
st.session_state["api_key"] = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# 確保在輸入 API 金鑰前無法使用其他功能
if not st.session_state["api_key"]:
    st.warning("Please enter your OpenAI API Key to continue.")
else:
    # 左側工具列選項
    with st.sidebar:
        st.header("Methods")
        st.session_state["selected_option"] = st.radio(
            "Please select a method:",
            ("JSON Schema", "Function Calling")
        )

    # 主界面標題和說明
    st.title("JSON Extractor Using GPT")
    st.write("Please input your message containing your name, email, and phone number.")

    # 根據選擇的模式顯示不同的輸入框和回應邏輯
    # 如果選擇 "JSON Schema" 方法
    if st.session_state["selected_option"] == "JSON Schema":
        st.subheader("JSON Schema Method")
        user_input = st.text_input("Please input your message:", key="json_schema_input")
        st.markdown(
            '<p style="font-size: 0.8em; color: gray;">For example: 我的名字是Stella，請用 stelladai1028@gmail.com 聯絡我，電話是0988999999</p>', 
            unsafe_allow_html=True
        )

        if st.button("Submit", key="json_schema_submit"):
            if user_input:
                # 添加使用者輸入到對話歷史
                st.session_state["conversation_history"].append({"role": "user", "content": user_input})
                
                # 傳入 api_key
                result = json_schema_response(user_input, st.session_state["conversation_history"], st.session_state["api_key"])
                if isinstance(result, UserData):
                    st.subheader("Answer")
                    st.json(result.model_dump())
                    # 將資料寫入 JSON 檔案
                    with open('user-data.json', 'a', encoding='utf-8') as f:
                        f.write(result.model_dump_json() + '\n')
                    st.success("Data successfully extracted and stored.")
                elif isinstance(result, str):
                    # 顯示特定的錯誤（如電子郵件格式錯誤）
                    st.error(result)
                else:
                    # 顯示一般輸入錯誤
                    st.error("Unable to extract valid data. Please check the input format.")

    # 如果選擇 "Function Calling" 方法
    elif st.session_state["selected_option"] == "Function Calling":
        st.subheader("Function Calling Method")
        user_input = st.text_input("Please input your message:", key="function_calling_input")
        st.markdown(
            '<p style="font-size: 0.8em; color: gray;">For example: Stella stelladai1028@gmail.com 0988999999</p>', 
            unsafe_allow_html=True
        )

        if st.button("Submit", key="function_calling_submit"):
            if user_input:
                # 添加使用者輸入到對話歷史
                st.session_state["conversation_history"].append({"role": "user", "content": user_input})
                
                # 傳入 api_key
                result = function_calling_response(user_input, st.session_state["conversation_history"], st.session_state["api_key"])
                if isinstance(result, UserData):
                    st.subheader("Answer")
                    st.json(result.model_dump())
                    # 將資料寫入 JSON 檔案
                    with open('user-data.json', 'a', encoding='utf-8') as f:
                        f.write(result.model_dump_json() + '\n')
                    st.success("Data successfully extracted and stored.")
                elif isinstance(result, str):
                    # 顯示特定的錯誤（如電子郵件格式錯誤）
                    st.error(result)
                else:
                    # 顯示一般輸入錯誤
                    st.error("Unable to extract valid data. Please check the input format.")

    # 顯示對話歷史
    st.subheader("Conversation History")
    if st.session_state["conversation_history"]:
        for entry in st.session_state["conversation_history"]:
            st.write(entry)
    else:
        st.write("No conversation history available.")
