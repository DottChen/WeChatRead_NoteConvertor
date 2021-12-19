# 用法：将程序放在markdown文件所在目录下，执行命令：python3 wechat_read_note_converter.py
# 原理：遍历当前目录下的所有markdown文件（由微信读书直接复制的笔记内容建立），将其文本转化为标准markdown格式并建立新文件
# -*- coding: utf-8 -*-

import os


# 通过打开系统目录读取原始markdown文件
def read_markdown_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


# 在换行的笔记前添加">> "
def add_symbol_to_note(data):
    lines = data.split('\n')
    for i in range(len(lines)):
        if lines[i] != '' and lines[i+1] != '' and lines[i][0] == '>':
            lines[i+1] = '>> ' + lines[i+1]
    return '\n'.join(lines)


# 替换data中的">>"为"-"（笔记），替换data中的"◆"为"###"（标题）
def replace_markdown_symbol(data):
    data = data.replace('>>', '-')
    data = data.replace('◆', '###')
    return data


# 在data中每一行不以"-"和"###"开头的有内容的正文（即自己的想法）前加上"> "作为引用
def add_markdown_symbol(data):
    lines = data.split('\n')
    for i in range(len(lines)):
        if lines[i] != '' and lines[i][0] != '-' and lines[i][0] != '#':
            lines[i] = '> ' + lines[i]
    return '\n'.join(lines)


# 删除空行
def delete_empty_line(data):
    lines = data.split('\n')
    for i in range(len(lines)-1, -1, -1):
        if lines[i] == '':
            del lines[i]
    return '\n'.join(lines)


# 删除内容重复的行
def delete_repeat_line(data):
    lines = data.split('\n')
    for i in range(len(lines)-1, -1, -1):
        for j in range(len(lines)-1, -1, -1):
            if i != j and lines[i] == lines[j]:
                del lines[i]
    return '\n'.join(lines)


# 除了前三行之外，将以"> "开头的行数与后面那行位置互换（将想法放到笔记后面）
def exchange_lines(data):
    lines = data.split('\n')
    jump = False
    for i in range(3, len(lines)-1):
        if jump:
            jump = False
            continue
        jump = True if lines[i][0] == '>' else False
        if lines[i][0] == '>':
            lines[i], lines[i+1] = lines[i+1], lines[i]
    return '\n'.join(lines)


# 将第一行的"> "替换为"# "（书籍名作为一级标题）
def replace_first_line(data):
    lines = data.split('\n')
    lines[0] = lines[0].replace('> ', '# ')
    return '\n'.join(lines)


# 将第二行与第三行互换位置，将此时第二行的"> "替换为"**（"，并在第二行末尾加上"）**"（调整作者的位置，加粗笔记数量）
def exchange_second_and_third_line(data):
    lines = data.split('\n')
    lines[1], lines[2] = lines[2], lines[1]
    lines[1] = lines[1].replace('> ', '**（') + '）**'
    return '\n'.join(lines)


# 将data写入以"原文件名+"+"_converted"+"md"的形式命名的新的markdown文件
def write_markdown_file(data, path):
    # 获取文件名
    file_name = os.path.basename(path)
    # 创建新的文件名
    new_file_name = file_name.replace('.md', '_converted.md')
    # 创建以新的文件名命名的markdown文件
    with open(new_file_name, 'w', encoding='utf-8') as f:
        f.write(data)


# 主程序
def main():
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    for file in files:
        if file.endswith('.md'):
            data = read_markdown_file(file)
            data = add_symbol_to_note(data)
            data = replace_markdown_symbol(data)
            data = add_markdown_symbol(data)
            data = delete_empty_line(data)
            data = delete_repeat_line(data)
            data = exchange_lines(data)
            data = replace_first_line(data)
            data = exchange_second_and_third_line(data)
            write_markdown_file(data, file)


if __name__ == '__main__':
    main()
