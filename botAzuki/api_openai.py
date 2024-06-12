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

client = OpenAI()

def setup_openai_logging():
    """
    配置专用于 OpenAI 操作的日志记录器。
    """
    # 定义日志格式和文件
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    log_filename = 'logs/openai_logs.txt'

    # 创建日志文件处理器
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))

    # 创建日志器
    logger = logging.getLogger('openai_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger

# 创建日志记录器
openai_logger = setup_openai_logging()

def ask_gpt_3x5(question):
    """
    使用 OpenAI GPT-3.5 模型回答问题。
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一名助手，负责解答我的各种问题。"},
                {"role": "user", "content": f"{question}"}
            ]
        )
        openai_logger.info(f"GPT-3.5 Request: {question}")
        return completion.choices[0].message.content
    except Exception as e:
        openai_logger.error(f"GPT-3.5 Error: {e}")
        return "Error in GPT-3.5 processing."

def ask_gpt_4x0(question):
    """
    使用 OpenAI GPT-4 模型回答问题。
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"你是一名活力满满的助手，非常乐于为我解答任何问题。"},
                {"role": "user", "content": f"{question}"}
            ]
        )
        openai_logger.info(f"GPT-4 Request: {question}")
        return completion.choices[0].message.content
    except Exception as e:
        openai_logger.error(f"GPT-4 Error: {e}")
        return "Error in GPT-4 processing."

def ask_gpt_4x0_kurisu(question):
    """
    使用 OpenAI GPT-4 模型回答问题。
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"你是一名傲娇的日系美少女，尽管你嘴上经常不情愿，但是实际上还是尽心为我解答任何问题。"},
                {"role": "user", "content": f"{question}"}
            ]
        )
        openai_logger.info(f"GPT-4 Request: {question}")
        return completion.choices[0].message.content
    except Exception as e:
        openai_logger.error(f"GPT-4 Error: {e}")
        return "Error in GPT-4 processing."

def audio2Text_openai(file_obj):

    """
    使用 OpenAI 将音频文件转换为文本。
    """
    try:

        if file_obj is None:
            return "未接收到音频文件"

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = f"audio/audio_{timestamp}.mp3"
        shutil.copyfile(file_obj, save_path)

        audio_file = open(save_path, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        openai_logger.info(f" {datetime.datetime.now()} - OPENAI GPT4语音转文字请求完成\n")

        return transcript
    except Exception as e:
        openai_logger.error(f"Audio to Text Error: {e}")
        return "Error in audio to text processing."

def text2Audio_openai(text):
    """
    使用 OpenAI 将文本转换为音频。
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    speech_file_path = f"audio/speech_{timestamp}.mp3"
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=f"{text}"
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path
    except Exception as e:
        openai_logger.error(f"Text to Audio Error: {e}")
        return "Error in text to audio processing."