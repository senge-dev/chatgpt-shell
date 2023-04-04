# chatgpt-shell
 
 使用Python语言编写的ChatGPT终端应用程序

## 介绍

ChatGPT Shell是一个支持ChatGPT的一个智能Linux Shell，支持ChatGPT对话和搜索等功能。

### API

ChatGPT Shell支持使用OpenAI官方API，同时也支持自建API服务，这里提供了一个自建API服务的教程：[ChatGPT API](https://chatgpt-api.pro/index.php/api/chatgpt-flask-api.html)

### OpenAI官方API

如果你不想自建API，也不想使用我搭建好的实例，你也可以使用OpenAI官方的API，但是可能需要配置代理服务器，如果你有代理服务器，请访问[OpenAI API](https://platform.openai.com/docs/guides/chat)

## 安装教程：

1. 安装Python3或更高版本

2. 安装python依赖库

```bash
pip install distro requests
```

3. 克隆GitHub仓库

```bash
git clone https://github.com/senge-dev/chatgpt-shell.git && cd chatgpt-shell
```

4. 配置ChatGPT Shell

按需修改配置文件

安装前编辑chatgpt-shell目录下的chatgpt.conf文件，修改配置项：

| 配置项 | 说明 | 备注|
| --- | --- | ---- |
| API_KEY | OpenAI 的 API 密钥 | 如果你没有API 密钥，请注册OpenAI账号，并访问[OpenAI API官网](https://platform.openai.com/)来创建你自己的API密钥 |
| API_URI | ChatGPT API请求地址 | 如果你想使用自建API，请修改为自建API的地址，如果你想使用OpenAI官方API，请直接修改为openai |
| SYSTEM_PROMPT | 系统提示信息 | 按需修改，${Distro} 为你当前的Linux发行版本，${UserName} 为你的用户名 |
| PROXY_URL | 代理服务器 | 如果你使用的是OpenAI官方的API，可能需要使用代理服务器 |
| PROXY_USERNAME | 代理服务器用户名 | 如果你的代理服务器需要验证，请填写此项 |
| PROXY_PASSWORD | 代理服务器密码 | 如果你的代理服务器需要验证，请填写此项 |

5. 安装ChatGPT Shell

```bash
chmod +x install.sh
./install.sh
```

6. 卸载ChatGPT Shell

```bash
chmod +x uninstall.sh
./uninstall.sh
```

## 使用教程：

### 切换ChatGPT Shell为默认Shell终端

```bash
chsh -s /usr/bin/chatgpt
```

### 常用命令

- 显示帮助信息

```bash
help
```

- 退出

```bash
exit
```

- 和ChatGPT对话

```bash
chat [message]
```

- 询问ChatGPT某个命令

```bash
search [command]
```

该参数会直接调用ChatGPT API来搜索命令，为了节省API额度，建议使用`man`命令来查询命令的使用方法。
