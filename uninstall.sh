#!/bin/bash

# 卸载脚本

# 建议使用非Root用户执行

if [ $(id -u) != "0" ]; then
    echo "不建议使用root用户执行卸载脚本"
    exit 1
fi

# 判断当前shell是否为chatgpt
if [ "$SHELL" == "/usr/bin/chatgpt" ]; then
    # 将shell替换为bash
    chsh -s /bin/bash
    if [ $? -eq 0 ]; then
        echo "设置成功"
    else
        echo "设置失败，请检查密码是否正确，为了防止系统出错，请先将Shell替换为ChatGPT以外的其他Shell，然后再进行卸载操作。"
        exit 1
    fi
fi

# 删除/etc/shells文件中 /usr/bin/chatgpt行
sudo sed -i '/\/usr\/bin\/chatgpt/d' /etc/shells

# 删除/usr/bin/chatgpt
sudo rm /usr/bin/chatgpt

# 删除/etc/chatgpt.conf

sudo rm /etc/chatgpt.conf

# 卸载完成
echo "卸载完成"
