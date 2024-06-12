
import gradio as gr
# 从其他模块导入必要的函数
from api_openai import ask_gpt_3x5, ask_gpt_4x0, audio2Text_openai, text2Audio_openai, ask_gpt_4x0_kurisu
from api_google import text2text_Request, image2Text_Request
from api_baidu import text2text_Baidu, text2Image_Baidu

# 定义全局变量
PRICING_TEXT = "截至15/01/2024，OpenAI公布的API计费标准为："
MARKDOWN_TABLE = """
                |      类型\模型    | GPT-4-Turbo 文本处理  | GPT-4-Turbo 视觉处理  |      GPT-3-Turbo     |
                | --------------- | ---------------------|---------------------|--------------------- |
                |        输入      | 0.01美元/每一千个Token | 0.01美元/每一千个Token | 0.001美元/每一千个Token|
                |        输出      | 0.03美元/每一千个Token | 0.03美元/每一千个Token | 0.001美元/每一千个Token|
                """
WARNING_TEXT = "N/A"

# 创建 Gradio 界面
with gr.Blocks(title="Project CloudAI") as demo:

    gr.Markdown("**Project CloudAI - Bot Beatrice 3.0**")
    gr.Markdown(PRICING_TEXT)
    gr.Markdown(MARKDOWN_TABLE)
    gr.Markdown("一个简单的中文问答通常会消耗1000-4000个Token（图文/语音处理则会更多），因此，对于简单的常规任务，推荐用户优先使用Gemini。")

    with gr.Tab("文生文(Google Gemini)"):
        with gr.Row():
            text_input_1 = gr.Textbox(label = "YOU")
            text_output_1 = gr.Textbox(label = "Bot_Beatrice")
        text2text_button = gr.Button("向Beatrice提问！")
        gr.Markdown("对于Gemini，建议使用英文提问（哪怕是机翻） ")

    with gr.Tab("图文提问(Google Gemini)"):
        with gr.Row():
            image_input_2 = gr.Image(label = "上传图片",type="pil")
            text_input_2 = gr.Textbox(label = "文本输入")
            text_output_2 = gr.Textbox(label = "解析结果")
        image2Text_button = gr.Button("向Beatrice提问！")
        gr.Markdown("对于Gemini，建议使用英文提问（哪怕是机翻） ")

    with gr.Tab("文生文(Baidu 文言一心)"):
        with gr.Row():
            text_input_3 = gr.Textbox(label = "YOU")
            text_output_3 = gr.Textbox(label = "Bot_Beatrice")
        text2text_button_baidu = gr.Button("向Beatrice提问！")

    with gr.Tab("文生图(Baidu 文言一心)"):
        with gr.Row():
            text_input_4 = gr.Textbox(label="YOU")
            image_output_4 = gr.Image(label = "响应结果",type="pil")
        gr.Markdown("如果文生图响应提示失败，通常是因为API的Token使用量超限，请联系管理员加钱扩容(´Д` ) ")
        text2Image_button_baidu = gr.Button("向Beatrice提问！")

    with gr.Tab("文生文(OpenAI GPT-3.5)"):
        with gr.Row():
            text_input_5 = gr.Textbox(label="YOU")
            text_output_5 = gr.Textbox(label = "Bot_Beatrice")
        gr.Markdown(WARNING_TEXT)
        gr.Markdown("如果ChatGPT提示失败，通常是因为预存金额被刷空了，请联系管理员加钱(´Д` ) ")
        text2Text_button_openai_3 = gr.Button("向Beatrice提问！")

    with gr.Tab("文生文(OpenAI GPT-4)"):
        with gr.Row():
            text_input_6 = gr.Textbox(label="在这里输入你的问题")
            text_output_6 = gr.Textbox(label = "Bot_Beatrice")
        gr.Markdown(WARNING_TEXT)
        gr.Markdown("如果ChatGPT提示失败，通常是因为预存金额被刷空了，请联系管理员加钱(´Д` ) ")
        gr.Markdown("注：由于训练数据和读取模式的不同，通过API请求的GPT-4的推理能力会略逊于ChatGPT Plus中的GPT-4，但仍然强于其他模型。 ")
        text2Text_button_openai_4 = gr.Button("向Beatrice提问！")

    with gr.Tab("语音文本转换(OpenAI Whisper)"):
        with gr.Row():
            text_input_7 = gr.Textbox(label="YOU")
            audio_output_7 = gr.Audio(label="Bot_Beatrice", type="filepath")
        text2Audio_button_openai_4 = gr.Button("让Beatrice讲话！")
        with gr.Row():
            audio_input_8 = gr.Audio(label="YOU", type="filepath")
            text_output_8 = gr.Textbox(label="Bot_Beatrice")
        audio2Text_button_openai_4 = gr.Button("向Beatrice讲话！")
        gr.Markdown(WARNING_TEXT)
        gr.Markdown("使用语音输入时，由于音频转码存在一定的处理延迟，建议隔2-5秒后再点击按钮。")
        gr.Markdown("如果ChatGPT提示失败，通常是因为预存金额被刷空了，请联系管理员加钱(´Д` ) ")
        
    with gr.Tab("文生文(Bot Kurisu - 基于GPT-4"):
        with gr.Row():
            text_input_10 = gr.Textbox(label="YOU")
            text_output_10 = gr.Textbox(label = "Bot_Kurisu")
        gr.Markdown(WARNING_TEXT)
        gr.Markdown("如果提示失败，通常是因为预存金额被刷空了，请联系管理员加钱(´Д` ) ")
        gr.Markdown("注：由于训练数据和读取模式的不同，通过API请求的GPT-4的推理能力会略逊于ChatGPT Plus中的GPT-4，但仍然强于其他模型。 ")
        text2Text_button_openai_4_2 = gr.Button("向Kurisu提问！")


    # 创建一个手风琴部分，包含一个Markdown文本
    with gr.Accordion("重要事项与基本介绍"):
        gr.Markdown("Project CloudAI是通过特定云服务商API所搭建的集成请求框架")
        gr.Markdown("如果点击“向Beatrice提问！”按钮后出现错误提示，可能是您或者服务器的网络出现了波动，请再次点击按钮生成内容。如果该问题仍然存在，请检查API对应的预存资金账户。")

    text2text_button.click(text2text_Request, inputs=text_input_1, outputs=text_output_1)
    image2Text_button.click(image2Text_Request, inputs=[image_input_2,text_input_2], outputs=text_output_2)
    text2text_button_baidu.click(text2text_Baidu, inputs=text_input_3, outputs=text_output_3)
    text2Image_button_baidu.click(text2Image_Baidu, inputs=text_input_4, outputs=image_output_4)
    text2Text_button_openai_3.click(ask_gpt_3x5, inputs=text_input_5, outputs=text_output_5)
    text2Text_button_openai_4.click(ask_gpt_4x0, inputs=text_input_6, outputs=text_output_6)
    text2Text_button_openai_4_2.click(ask_gpt_4x0_kurisu, inputs=text_input_10, outputs=text_output_10)
    audio2Text_button_openai_4.click(audio2Text_openai, inputs=audio_input_8, outputs=text_output_8)
    text2Audio_button_openai_4.click(text2Audio_openai, inputs=text_input_7, outputs=audio_output_7)


# 启动 Gradio 应用
if __name__ == "__main__":
    demo.launch(share=True)