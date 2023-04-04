#!/bin/bash

# 安装脚本

# 建议非Root用户运行，如果是Root，则提示警告信息

if [ $(id -u) == "0" ]; then
    echo "警告：建议不要使用root用户来完成安装"
    read -p "确定要以root用户来完成安装？[yes/no]：" isroot
    if [ "$isroot" != "yes" ]; then
        echo "安装已取消"
        exit 0
    fi
fi

# 安装目录：
# Shell文件： /usr/bin/chatgpt
# 配置文件目录： /etc/chatgpt.conf
# 修改/etc/shells文件，添加Shell可执行文件
# 提示用户在安装前修改配置文件
echo "请修改配置文件，当您修改完成后输入yes来继续安装"
read -p "是否继续？[yes/no]：" iscontinue
if [ "$iscontinue" != "yes" ]; then
    echo "安装已取消"
    exit 0
fi
# 安装程序
echo "正在安装程序..."
# 将chatgpt文件复制到/usr/bin/chatgpt
sudo cp chatgpt.py /usr/bin/chatgpt
# 赋予可执行权限（针对所有用户）
sudo chmod a+x /usr/bin/chatgpt
# 复制配置文件
sudo cp chatgpt.conf /etc/chatgpt.conf
# 判断/etc/shell中是否已经存在 /usr/bin/chatgpt
if [ $(grep -c "/usr/bin/chatgpt" /etc/shells) -eq 0 ]; then
    # 如果不存在，则添加
    echo "/usr/bin/chatgpt" | sudo tee -a /etc/shells
fi

# 安装完成，让用户选择是否将chatgpt设置为默认Shell
echo "安装完成"
read -p "是否将chatgpt设置为默认Shell？[yes/no]：" issetshell
if [ "$issetshell" == "yes" ]; then
    # 设置chatgpt为默认Shell
    chsh -s /usr/bin/chatgpt
    if [ $? -eq 0 ]; then
        echo "设置成功"
    else
        echo "设置失败，请检查密码是否正确，如果您后续想要设置chatgpt为默认Shell，请运行chsh -s /usr/bin/chatgpt命令"
    fi
fi
