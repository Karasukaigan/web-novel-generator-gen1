import json
import os
import re
from datetime import datetime
from openai import *

# 测试小说配置是否正确
def validate_novel_config(novel_config):
    errors = []
    if not novel_config.get('plot_summary'):
        errors.append("[error] plot_summary is missing")
    if not novel_config.get('total_chapters') or novel_config['total_chapters'] < 1:
        errors.append("[error] total_chapters must be a positive integer greater than 0")
    if not novel_config.get('words_per_chapter') or novel_config['words_per_chapter'] < 500:
        errors.append("[error] words_per_chapter must be an integer greater than or equal to 500")
    if errors:
        for error in errors:
            print(error)
        return False
    else:
        return True

# 测试API配置是否正确
def test_api_connection(base_url, api_key, model):
    client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, world!"}
            ]
        )
        print("[success] API connection successful:", completion.choices[0].message.content)
        return True
    except Exception as e:
        print(f"[error] API connection failed: {e}")
        return False

# 读取JSON文件并返回字典
def read_json_to_dict(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"[error] Failed to read JSON file: {e}")
        return None

# 将字典保存为JSON文件
def write_dict_to_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"[write] {file_path}")
    except Exception as e:
        print(f"[error] Failed to write to JSON file: {e}")

# 读取TXT文件并返回字符串
def read_txt_to_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"[error] Failed to read TXT file: {e}")
        return None

# 将字符串保存为TXT文件
def write_string_to_txt(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
        print(f"[write] {file_path}")
    except Exception as e:
        print(f"[error] Failed to write to TXT file: {e}")

# 更新用量信息
def update_usage_log(usage, base_url, model):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f'{{ "base_url": "{base_url}", "model": "{model}", "completion_tokens": {usage["completion_tokens"]}, "prompt_tokens": {usage["prompt_tokens"]}, "total_tokens": {usage["total_tokens"]}, "timestamp": "{timestamp}" }}\n'
    try:
        with open('usage.log', 'a') as file:
            file.write(log_entry)
    except Exception as e:
        print(f"[error] Failed to write to usage.log: {e}")

# 缩略显示文本
def summarize_text(text):
    if len(text) > 50:
        return text[:20] + "..." + text[-20:]
    else:
        return text

# 获取最后20个字符
def get_last_20_chars(text):
    if len(text) > 20:
        return text[-20:]
    else:
        return text

# 从Markdown中提取文本
def extract_sections(markdown_string):
    markdown_string = markdown_string.replace('```', '').replace('markdown', '')
    titles = []
    sections = []
    current_section = []
    lines = markdown_string.splitlines()
    for line in lines:
        if line.startswith("## "):
            if current_section:
                sections.append("\n".join(current_section).strip())
                current_section = []
            title = line[3:]
            titles.append(title.strip())
        current_section.append(line)
    if current_section:
        sections.append("\n".join(current_section).strip())
    cleaned_sections = [re.sub(r'^## .+\n?', '', section).strip() for section in sections]
    return {"titles": titles, "sections": cleaned_sections}

# 合并字符串
def merge_strings_with_newlines(string_array):
    merged_string = '\n\n\n'.join(string_array)
    return merged_string

# 为各部分分配章节数
def split_chapters(total_chapters, parts):
    base_chapters = total_chapters // parts
    extra_chapters = total_chapters % parts
    distribution = []
    for i in range(parts):
        if i < extra_chapters:
            distribution.append(base_chapters + 1)
        else:
            distribution.append(base_chapters)
    distribution.reverse()
    return distribution

# 拼接字符串数组中最后n个字符串
def concatenate_last_n(strings, n):
    if len(strings) < n:
        return '\n\n'.join(strings)
    else:
        return '\n\n'.join(strings[-n:])

if __name__ == '__main__':
    pass