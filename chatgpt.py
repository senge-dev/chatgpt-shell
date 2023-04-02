#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import requests
from configparser import ConfigParser as Ini
import subprocess
import distro
import readline


class ChatGPT:

    def __init__(self, api_key, system_prompt="", url="https://chatgpt.example.com", max_tokens=100):
        """初始化ChatGPT Shell
        :param api_key: API Key
        :param system_prompt: 系统提示
        :param url: API URL，搭建教程详见：https://chatgpt-api.pro/index.php/api/chatgpt-flask-api.html
        :param max_tokens: 每次回复的最大Token数
        """
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.url = url
        self.max_tokens = max_tokens
        self.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    def send_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        data = {
            "api_key": self.api_key,
            "system_content": self.system_prompt,
            "user_content": message,
            "continuous": self.messages,
            "max_tokens": self.max_tokens,
            "model": "gpt-3.5-turbo"
        }
        result = requests.post(self.url, json=data)
        if result.status_code == 200:
            response = result.json()
            chatgpt_reply = response['current_response']
            self.messages.append({
                "role": "assistant",
                "content": chatgpt_reply
            })
            return chatgpt_reply
        else:
            print("Error: ", result.status_code)
            print(result.text)
            return None
    
    def commit_message(self, user_content, chatgpt_reply):
        self.messages.append({
            "role": "user",
            "content": user_content
        })
        self.messages.append({
            "role": "assistant",
            "content": chatgpt_reply
        })


if __name__ == "__main__":
    # 从配置文件读取 API Key、系统提示、URL、最大Token数
    conf = Ini()
    conf.read("/etc/chatgpt.conf")
    api_key = conf.get("common", "API_KEY")
    system_prompt = conf.get("common", "SYSTEM_PROMPT").replace("${UserName}", os.getlogin()).replace("${Distro}", distro.name())
    url = conf.get("common", "API_URI")
    max_tokens = conf.getint("common", "MAX_TOKENS")
    # 初始化ChatGPT Shell
    chatgpt = ChatGPT(api_key, system_prompt, url, max_tokens)
    distribution = distro.name()
    kernel_version = os.uname().release
    username = os.getlogin()
    hostname = os.uname().nodename
    print(f"""
 ██████╗██╗  ██╗ █████╗ ████████╗ ██████╗ ██████╗ ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝ ██╔══██╗╚══██╔══╝
██║     ███████║███████║   ██║   ██║  ███╗██████╔╝   ██║   
██║     ██╔══██║██╔══██║   ██║   ██║   ██║██╔═══╝    ██║   
╚██████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║        ██║   
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝        ╚═╝   
 
 您好，{username}！欢迎使用ChatGPT Shell，您的计算机信息：
    操作系统：{distribution}
    内核版本：{kernel_version}
    用户名：{username}
    主机名：{hostname}

    如需帮助，请输入help
    """)
    failed = False
    # 设置历史记录长度
    readline.set_history_length(1000)
    try:
        readline.read_history_file(os.path.expanduser('~/.chatgpt_history'))
    except FileNotFoundError:
        pass
    while True:
        try:
            # 获取用户的输入
            print(f"{'(x)' if failed else ''} ChatGPT {'#' if os.getuid() == 0 else '$'}", end="\n> ")
            # readline.set_pre_input_hook(pre_input_hook)
            user_input = input()
            readline.write_history_file(os.path.expanduser('~/.chatgpt_history'))
            # 判断用户输入
            if user_input.startswith("chat "):
                message = user_input[5:]
                chatgpt_reply = chatgpt.send_message(message)
                if chatgpt_reply is not None:
                    print(chatgpt_reply)
            elif user_input.startswith("search "):
                command = user_input[7:]
                chatgpt_reply = chatgpt.send_message(f"{command}命令的作用是什么？如何使用和安装这个命令？")
                if chatgpt_reply is not None:
                    print(chatgpt_reply)
            elif user_input == "exit":
                print("程序已退出")
                sys.exit(0)
            elif user_input == "help":
                print(f"""您好，{username}，这里是ChatGPT Shell的专用命令
        [command] 直接执行命令
        chat [message] 与ChatGPT进行对话（支持连续对话）
        exit 退出ChatGPT Shell
        help 查看帮助信息
        history 查看历史命令
        search [command] 在ChatGPT Shell中搜索某个命令，例如：search command 将会搜索到command命令的使用/安装方法。
            """)
            elif user_input == "history":
                for i in range(1, readline.get_current_history_length() + 1):
                    print(f"{i}  {readline.get_history_item(i)}")
            elif user_input.startswith("cd "):
                path = user_input[3:]
                if path.startswith("~"):
                    path = os.path.expanduser(path)
                if path.startswith("./"):
                    path = os.path.abspath(path)
                if path.startswith("../"):
                    path = os.path.abspath(path)
                if os.path.exists(path):
                    os.chdir(path)
                else:
                    print(f"cd: {path}: 没有那个文件或目录")
            else:
                # 执行命令
                try:
                    cmd = f"{user_input}"
                    result = subprocess.run(user_input, shell=True)
                    if result.returncode == 0:
                        failed = False
                    else:
                        failed = True
                except subprocess.TimeoutExpired:
                    print("命令执行超时")
                    failed = True
                except FileNotFoundError:
                    print("命令不存在")
                    failed = True
                except Exception as e:
                    print(e)
                    failed = True
        except KeyboardInterrupt:
            failed = True
            continue
        except EOFError:
            print("程序已退出")
            sys.exit(0)


