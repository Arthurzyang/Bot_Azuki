import numpy as np
import gradio as gr
from PIL import Image
import io
import requests
import json
import os
import time
import logging
import datetime
import base64
import json
import soundfile as sf
import requests
import pathlib
import textwrap
import google.generativeai as genai
import erniebot
import shutil
from openai import OpenAI
from pydub import AudioSegment


# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/google_logs.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


#API KEYS
API_KEY = ""
with open('api_keys/ac.txt', 'r', encoding='utf-8') as file:
    API_KEY = file.read()
IMAGE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=" + API_KEY


def text2text_Request(text):

    """
    使用 Google Gemini API 将文本转换为文本。
    """
    try:

        url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + API_KEY

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": text}]
                }
            ]
        }
        response = requests.post(url, json=payload)
        response_json = response.json()
        gemini_text = response_json['candidates'][0]['content']['parts'][0]['text']

        logger.info(f"Text to Text request processed for text: {text}")
        return gemini_text
    except Exception as e:
        logger.error(f"Text to Text Error: {e}")
        return "Error in text to text processing."


def image2Text_Request(pil_image, prompt):
    """
    使用 Google Gemini API 将图像和文本转换为文本。
    """
    try:

        # 创建img_to_text文件夹，如果它不存在
        output_folder = "img_to_text"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # 构建保存路径
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = os.path.join(output_folder, f"image_{timestamp}.jpeg")
        # 将PIL图像保存到指定路径
        pil_image.save(save_path, format='JPEG')

        # 将PIL图像转换成Base64编码
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG')  # 保存为JPEG格式
        img_byte_arr = img_byte_arr.getvalue()
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

        # 组织JSON请求体
        json_input = json.dumps({
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_base64
                            }
                        }
                    ]
                }
            ]
        })
        # 发送POST请求
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=" + API_KEY
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json_input)

        # 打印响应内容
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            # 提取text字段的值
            text_value = response_dict["candidates"][0]["content"]["parts"][0]["text"]
            logger.info(f"{datetime.datetime.now()}\n图生文请求提示词: {prompt} - \n服务器响应: {text_value}\n")
            return text_value
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        logger.error(f"Image to Text Error: {e}")
        return "Error in image to text processing."
