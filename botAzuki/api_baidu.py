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


# 设置日志记录
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/baidu_logs.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# API Keys
API_TYPE_BAIDU="aistudio"
API_KEY_BAIDU = ""
with open('api_keys/baidu.txt', 'r', encoding='utf-8') as file:
    API_KEY_BAIDU = file.read()

API_TYPE_YINIAN = "yinian"
API_KEY_YINIAN = ""
with open('api_keys/yinian.txt', 'r', encoding='utf-8') as file:
    API_KEY_YINIAN = file.read()
SK_YINIAN = ""
with open('api_keys/sk.txt', 'r', encoding='utf-8') as file:
    SK_YINIAN = file.read()


def get_access_token():

    """
    获取百度API的访问令牌
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY_YINIAN, "client_secret": SK_YINIAN}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        logger.error(f"Failed to get access token: {response.text}")
        return None


def text2text_Baidu(text):

    """
    使用百度API将文本转换为文本。
    """
    try:
        # 实现百度文本到文本的API调用
        response = erniebot.ChatCompletion.create(
            _config_=dict(
                api_type=API_TYPE_BAIDU,
                access_token=API_KEY_BAIDU,
            ),
            model="ernie-bot",
            messages=[{"role": "user", "content": f"{text}",
                       }],
        )
        logger.info(f" {datetime.datetime.now()} \n文言一心文生文请求提示词: {text} - \n服务器响应: {response.result}\n")
        return response.result
    except Exception as e:
        logger.error(f"Text to Text Error: {e}")
        return "Error in text to text processing."


def text2Image_Baidu(text):

    """
    使用百度API将文本转换为图像。
    """
    try:
        url = "https://aip.baidubce.com/rpc/2.0/ernievilg/v1/txt2img?access_token=" + get_access_token()

        payload = json.dumps({
            "text": f"{text}",
            "resolution": "1024*1024",
            "style": "写实风格"
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info(f" {datetime.datetime.now()} \n文生文请求提示词: {text} - \n服务器响应: {response.text}\n")
        dataTraceId = json.loads(response.text)
        task_id = dataTraceId['data']['taskId']
        logger.info(f" {datetime.datetime.now()} \ntaskId=: {task_id}\n")

        urlGetImg = "https://aip.baidubce.com/rpc/2.0/ernievilg/v1/getImg?access_token=" + get_access_token()
        payloadGetImg = json.dumps({"taskId": task_id})
        headersGetImg = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        counter = 1;
        responseGetImg = requests.request("POST", urlGetImg, headers=headersGetImg, data=payloadGetImg)
        logger.info(
            f" {datetime.datetime.now()} \n第{counter}次请求：taskId: {task_id} - \n服务器响应: {responseGetImg.text}\n")
        data = json.loads(responseGetImg.text)

        status = data['data']['status']
        while status == 0 and counter < 10:
            time.sleep(3)
            responseGetImg = requests.request("POST", urlGetImg, headers=headersGetImg, data=payloadGetImg)
            logger.info(
                f" {datetime.datetime.now()} \n第{counter}次请求：taskId: {task_id} - \n服务器响应: {responseGetImg.text}\n")
            data = json.loads(responseGetImg.text)
            status = data['data']['status']
            counter += 1

        img_url = data['data']['imgUrls'][0]['image']
        print(img_url)
        img_data = requests.get(img_url).content
        with open(f'imgBaidu/{task_id}.jpg', 'wb') as f:
            f.write(img_data)
        # 使用 PIL 打开本地文件
        reImage = Image.open(f'imgBaidu/{task_id}.jpg')
        return reImage
    except Exception as e:
        logger.error(f"Text to Image Error: {e}")
        return "Error in text to image processing."
