#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import requests
from configparser import ConfigParser as Ini
import configparser
import subprocess
import distro
import readline


class ChatGPT:

    def __init__(self, api_key, system_prompt="", url="https://chatgpt.example.com", max_tokens=100, proxy_url=None, proxy_username=None, proxy_password=None):
        """初始化ChatGPT Shell
        :param api_key: API Key
        :param system_prompt: 系统提示
        :param url: API URL，搭建教程详见：https://chatgpt-api.pro/index.php/api/chatgpt-flask-api.html，如果不想使用自己搭建的API，可以将URL设置为openai来使用OpenAI的API（可能需要配置代理）
        :param max_tokens: 每次回复的最大Token数
        :param proxy_url: 代理URL，如果不想使用代理，可以将其设置为null
        :param proxy_username: 代理用户名
        :param proxy_password: 代理密码
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
        self.proxy_url = proxy_url
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password

    def send_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        if self.url == "openai" or self.url.startswith("https://api.openai.com") or self.url.startswith("https://openai.com"):
            data = {
                "messages": self.messages,
                "max_tokens": self.max_tokens,
                "model": "gpt-3.5-turbo"
            }
        else:
            data = {
                "api_key": self.api_key,
                "system_content": self.system_prompt,
                "user_content": message,
                "continuous": self.messages,
                "max_tokens": self.max_tokens,
                "model": "gpt-3.5-turbo"
            }
        
        if self.proxy_url is not None:
            proxies = {
                "http": self.proxy_url,
                "https": self.proxy_url
            }
            if self.proxy_username is not None and self.proxy_password is not None:
                proxies["http"] = self.proxy_username + ":" + self.proxy_password + "@" + self.proxy_url
                proxies["https"] = self.proxy_username + ":" + self.proxy_password + "@" + self.proxy_url
            result = requests.post(self.url, json=data, headers=headers, proxies=proxies)
        else:
            result = requests.post(self.url, json=data, headers=headers)
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
    username = os.popen("whoami").read().strip()
    system_prompt = conf.get("common", "SYSTEM_PROMPT").replace("${UserName}", username).replace("${Distro}", distro.name())
    url = conf.get("common", "API_URI")
    max_tokens = conf.getint("common", "MAX_TOKENS")
    try:
        proxy_url = conf.get("proxy", "PROXY_URL")
        proxy_username = conf.get("proxy", "PROXY_USERNAME")
        proxy_password = conf.get("proxy", "PROXY_PASSWORD")
    except (configparser.NoSectionError, configparser.NoOptionError):
        # print("No Proxy")
        proxy_url = None
        proxy_username = None
        proxy_password = None
        # chatgpt = ChatGPT(api_key, system_prompt, url, max_tokens)
    finally:
        # 初始化ChatGPT Shell(设置代理)
        # print("Proxy")
        chatgpt = ChatGPT(api_key, system_prompt, url, max_tokens, proxy_url, proxy_username, proxy_password)
    distribution = distro.name()
    kernel_version = os.uname().release
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
        exec [message] 使用自然语言的方式执行命令：例如：exec 列出当前目录下的文件，包括隐藏文件，此时ChatGPT将会执行ls -a命令。
        history 查看历史命令
        search [command] 在ChatGPT Shell中搜索某个命令，例如：search command 将会搜索到command命令的使用/安装方法。
        whatswrong [filename]  读取源代码文件，检查源代码的语法错误，并提供修复建议。
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
            elif user_input.startswith("whatswrong "):
                # 判断文件是否存在
                filename = user_input[11:]
                if not os.path.exists(filename):
                    print(f"whatswrong: {filename}: 没有那个文件或目录")
                    continue
                else:
                    # 读取文件
                    with open(filename, "r") as f:
                        code = f.read()
                    # 检查文件
                    reply = chatgpt.send_message(f"我编写了一段源代码，但是不知道是否有语法错误，请你帮我检查一下。源代码内容：\n\n {code}")
                    if reply is not None:
                        print(reply)
            elif user_input.startswith("exec "):
                # 判断文件是否存在
                message = user_input[5:]
                reply = chatgpt.send_message(f"我想要{message}，请你直接给出命令，不要对内容进行复述，不要回复任何其他内容，由于我要将你的回答传递给计算机进行执行，如果你回答了其他内容，将会执行失败。注意：1. 如果命令必须以root身份执行，请在命令前加上sudo（例如某些发行版本使用包管理器安装应用）。\n2. 如果命令有危险性，请拒绝执行，并使用echo命令输出该命令存在的风险。\n3. 以下为示例：\n列出当前目录下的文件，包括隐藏文件\tls -a\n查看Linux内核版本\tuname -r\n切换为root用户\tsudo su")
                if reply is not None:
                    # 执行命令
                    print(f"根据你的回复，我将执行命令：{reply}")
                    try:
                        result = subprocess.run(reply, shell=True)
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
            else:
                # 执行命令
                try:
                    cmd = f"{user_input}"
                    result = subprocess.run(cmd, shell=True)
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

