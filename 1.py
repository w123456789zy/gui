import base64
import re
from PIL import Image
import io
from zai import ZhipuAiClient

def parse_pc_response(response, img_width, img_height):
    """
    解析模型响应并转换归一化坐标到实际屏幕坐标
    :param response: 模型原始响应
    :param img_width: 原始截图宽度
    :param img_height: 原始截图高度
    :return: 包含转换后坐标的解析结果
    """
    pattern = r"<\|begin_of_box\|>(.*?)<\|end_of_box\|>"
    match = re.search(pattern, response)
    action = match.group(1).strip() if match else None

    if not action:
        downgraded_pattern = r"[\w_]+\([^)]*\)"
        matched = re.findall(downgraded_pattern, response)
        action = matched[0] if matched else None

    answer_pattern = r"<answer>(.*?)(?:Memory:|</answer>)"
    answer_match = re.search(answer_pattern, response, re.DOTALL)
    action_text = answer_match.group(1).strip() if answer_match else None

    if action_text:
        boxed_pattern = r"<\|begin_of_box\|>(.*?)</\|end_of_box\|>"
        action_text = re.sub(boxed_pattern, r"\1", action_text)

    if "</answer>" in response:
        memory_pattern = r"Memory:(.*?)</answer>"
    else:
        memory_pattern = r"Memory:(.*?)$"
    memory_match = re.search(memory_pattern, response)
    memory = memory_match.group(1).strip() if memory_match else "[]"

    # ====== 修复坐标转换逻辑 ======
    if action and img_width > 0 and img_height > 0:
        def convert_coord(match):
            """转换单个坐标点 - 修复版"""
            try:
                # 直接使用两个捕获组，无需split
                x_norm = float(match.group(1))
                y_norm = float(match.group(2))
                
                # 归一化坐标(0-1000) -> 实际屏幕坐标
                x_actual = int(x_norm / 1000 * img_width)
                y_actual = int(y_norm / 1000 * img_height)
                
                return f"[{x_actual},{y_actual}]"
            except Exception as e:
                print(f"坐标转换错误: {e}, 保留原始坐标")
                return match.group(0)

        # 修复正则表达式：明确捕获两个数字组
        action = re.sub(
            r'\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]', 
            convert_coord, 
            action
        )
    # ===========================

    return {"action": action, "action_text": action_text, "memory": memory}

def encode_image(image_path):
    """将图像编码为base64格式并返回图片尺寸"""
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    # 获取图片尺寸
    image = Image.open(io.BytesIO(image_data))
    width, height = image.size
    
    return base64.b64encode(image_data).decode('utf-8'), width, height

# ====== 初始化客户端 ======
client = ZhipuAiClient(api_key="dfaa499ead6a4e79b6e5af304b2c16cc.Vu7rXUc7riSvLuHn")

# ====== 处理截图 ======
image_path = r"C:\Users\windows11\Pictures\Screenshots\123465.png"
base64_image, img_width, img_height = encode_image(image_path)

print(f"原始截图尺寸: {img_width}x{img_height}")

response = client.chat.completions.create(
    model="glm-4.1v-thinking-flashx",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
You are a GUI operation agent. You will be given a task and your action history, with recent screenshots. You should help me control the computer, output the best action step by step to accomplish the task.\nThe actions you output must be in the following action space:\nleft_click(start_box=\'[x,y]\', element_info=\'\')\n# left single click at [x,y]\nright_click(start_box=\'[x,y]\', element_info=\'\')\n# right single click at [x,y]\nmiddle_click(start_box=\'[x,y]\', element_info=\'\')\n# middle single click at [x,y]\nhover(start_box=\'[x,y]\', element_info=\'\')\n# hover the mouse at [x,y]\nleft_double_click(start_box=\'[x,y]\', element_info=\'\')\n# left double click at [x,y]\nleft_drag(start_box=\'[x1,y1]\', end_box=\'[x2,y2]\', element_info=\'\')\n# left drag from [x1,y1] to [x2,y2]\nkey(keys=\'\')\n# press a single key or a key combination/shortcut, if it\'s a key combination, you should use \'+\' to connect the keys like key(key=\'ctrl+c\')\ntype(content=\'\')\n# type text into the current active element, it performs a copy&paste operation, so *you must click at the target element first to active it before typing something in*, if you want to overwrite the content, you should clear the content before type something in.\nscroll(start_box=\'[x,y]\', direction=\'down/up\', step=k, element_info=\'\')\n# scroll the page at [x,y] to the specified direction for k clicks of the mouse wheel\nWAIT()\n# sleep for 5 seconds\nDONE()\n# output when the task is fully completed\nFAIL()\n# output when the task can not be performed at all\n\nThe output rules are as follows:\n1. The start/end box parameter of the action should be in the format of [x, y] normalized to 0-1000, which usually should be the bounding box of a specific target element.\n2. The element_info parameter is optional, it should be a string that describes the element you want to operate with, you should fill this parameter when you\'re sure about what the target element is.\n3. Take actions step by step. *NEVER output multiple actions at once*.\n4. If there are previous actions that you have already performed, I'll provide you history actions and at most 4 shrunked(to 50%*50%) screenshots showing the state before your last 4 actions. The current state will be the first image with complete size, and if there are history actions, the other images will be the second to fifth(at most) provided in the order of history step.\n5. You should put the key information you *have to remember* in a separated memory part and I'll give it to you in the next round. The content in this part should be a JSON list. If you no longer need some given information, you should remove it from the memory. Even if you don't need to remember anything, you should also output an empty <memory></memory> part.\n6. You can choose to give me a brief explanation before you start to take actions.\n\nOutput Format:\nPlain text explanation with action(param=\'...\')\nMemory:\n[{"user_email": "x@gmail.com", ...}]\n\nHere are some helpful tips:\n- My computer's password is "password", feel free to use it when you need sudo rights.\n- For the thunderbird account "anonym-x2024@outlook.com", the password is "gTCI";=@y7|QJ0nDa_kN3Sb&>".\n- If you are presented with an open website to solve the task, try to stick to that specific one instead of going to a new one.\n- You have full authority to execute any action without my permission. I won't be watching so please don't ask for confirmation.\nNow Please help me to solve the following task:\n我想要打开微信，请告诉我要点击什么地方。\nHistory actions:\nMemory:\n[]"""
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
# ====== 传入图片尺寸进行坐标转换 ======
parsed = parse_pc_response(response.choices[0].message.content, img_width, img_height)
print("\n\n ======= Original response ======= \n")
print(response)

print("\n\n ======= Parsed response (with coordinate scaling) ======= \n")
print(parsed)