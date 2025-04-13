import json
import os
import random
from openai import *
from src.tools import *
from src.max_tokens import *

# 生成小说名
def generate_novel_title(api_config, plot_summary):
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。你本次的任务是根据小说的相关信息为其起一个有创意且能够吸引目标读者的小说名。"},
        {"role": "user", "content": f"请基于以下信息为这部小说起一个名字。请只输出小说名，不要有额外回答，不要加书名号。剧情简介：{plot_summary}"}
    ]
    print(f'[info] Naming the novel...')
    return call_openai_api(api_config, messages, 50)

# 判断小说类型
def determine_novel_genre(api_config, plot_summary):
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。你本次的任务是根据小说的相关信息判断其类型。常见的小说类型包括但不限于：玄幻、奇幻、武侠、仙侠、都市、言情、历史、军事、悬疑、灵异、科幻、游戏、同人、现实、穿越、重生、末世、无限流、系统流、随身空间流、种田文、总裁文、宫斗、宅斗、校园、职场、娱乐、竞技、美食、旅游、探险、盗墓、修真、魔法、异能、机甲。"},
        {"role": "user", "content": f"请基于以下剧情简介，确定这部小说的类型。请只输出小说类型，不添加任何额外的文字或标点符号。剧情简介：{plot_summary}"}
    ]
    print(f'[info] Determining the novel genre...')
    return call_openai_api(api_config, messages, 20)

# 扩写剧情简介
def expand_plot_summary(api_config, plot_summary):
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。你本次的任务是完善剧情简介，确保剧情简介涵盖故事的开端、发展、高潮和结局，且包含显性冲突与潜在危机，体现人物核心驱动力。"},
        {"role": "user", "content": f"请完善以下剧情简介。只输出剧情简介内容，不要添加任何额外注释或说明。以下是原始的剧情简介：{plot_summary}"}
    ]
    print(f'[info] Expanding the plot summary...')
    return call_openai_api(api_config, messages, get_max_tokens(api_config['model']))

# 润色剧情简介
def refine_plot_summary(api_config, plot_summary):
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。你本次的任务是润色、精炼剧情简介，精炼到150字左右，简介里不能透露小说结局，要留下悬念，确保剧情简介能尽可能吸引读者，且让网文平台编辑觉得这个作品有爆款潜力。"},
        {"role": "user", "content": f"请润色以下剧情简介。只输出剧情简介内容，不要添加任何标题、标签、额外注释或说明。以下是原始的剧情简介：{plot_summary}"}
    ]
    print(f'[info] Refining the plot summary...')
    return call_openai_api(api_config, messages, get_max_tokens(api_config['model']))

# 生成世界观设定
def generate_world_setting(api_config, novel_config):
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。你本次的任务是根据小说的相关信息对其世界观做出设定，构建一个为核心冲突服务的三维交织的世界观。世界观需要基于以下三个维度：物理维度（空间、时间等）、社会维度（权力结构、文化、经济等）、隐喻维度（气候、环境、反复出现的意象等）。"},
        {"role": "user", "content": f"这本小说叫《{novel_config['novel_title']}》，类型是{novel_config['novel_genre']}。请基于剧情简介构建世界观。请只回答世界观内容，不要添加任何额外注释或说明。以下是剧情简介：{novel_config['plot_summary_expand']}"}
    ]
    print(f'[info] Generating world setting...')
    return call_openai_api(api_config, messages, get_max_tokens(api_config['model']))

# 生成角色设定
def generate_character_settings(api_config, novel_config):
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。你本次的任务是根据小说的相关信息设计5到20个具有动态变化潜力的核心角色，具体数量根据小说字数动态决定，例如10万字需要5个核心角色，100万字需要10个核心角色，1000万字需要20个核心角色。"},
        {"role": "user", "content": f"这本小说叫《{novel_config['novel_title']}》，约{round(novel_config['total_chapters'] * novel_config['words_per_chapter'] * 1.2)}字、共{novel_config['total_chapters']}章，类型是{novel_config['novel_genre']}。请基于剧情简介、世界观和小说字数设计多个核心角色。要求每个角色都要有具体名字（如果小说相关信息里没有的话则想一个），还需包含背景、外貌、性别、年龄、职业、秘密、潜在弱点(可与世界观或其他角色有关)等特征，还要写明核心驱动力三角：表面追求（物质目标）、深层渴望（情感需求）、灵魂需求（哲学层面）。请只回答角色设定，不要添加任何额外注释或说明。- 剧情简介：{novel_config['plot_summary_expand']}\n\n- 世界观：\n{novel_config['world_setting']}"}
    ]
    print(f'[info] Generating character settings...')
    return call_openai_api(api_config, messages, get_max_tokens(api_config['model']))

# 生成剧情大纲
def generate_plot_outline(api_config, novel_config):
    total_characters = round(novel_config['total_chapters'] * novel_config['words_per_chapter'] * 1.2) # 总字数
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。你本次的任务是根据小说的相关信息规划出吸引人的具有爆款潜力的剧情大纲。"},
        {"role": "user", "content": f"我会先给你关于小说的一些信息，然后你再根据这些信息来规划剧情大概。这是一本约{total_characters}字、共{novel_config['total_chapters']}章的小说，名叫《{novel_config['novel_title']}》，类型是{novel_config['novel_genre']}。以下是剧情简介：{novel_config['plot_summary_expand']}"},
        {"role": "assistant", "content": "已收到，是否还有别的信息？"},
        {"role": "assistant", "content": f"以下是小说世界观设定：\n{novel_config['world_setting']}"},
        {"role": "assistant", "content": "已收到，是否还有别的信息？"},
        {"role": "assistant", "content": f"以下是小说人物设定：\n{novel_config['character_settings']}"},
        {"role": "assistant", "content": "已收到，是否还有别的信息？"},
        {"role": "user", "content": f"没有了。请基于以上提供给你的剧情简介、人物设定，设计一个合理的剧情大纲，将故事分为5到30个相对独立又互相关联的Part（具体数量根据小说总字数而定，例如十万字要分成5个Part、一百万字要分成20个Part、一千万字要分成30个Part），请合理控制剧情发展的速度，均匀分布到各个Part，每个Part都要有相对独立的爽文故事，且不能与之前的剧情重复。请使用Markdown格式进行编写，每个Part都以二级标题（即“## ”开头）的形式单独列出，并紧跟该部分的200字描述（话语要精炼）。请只回答大纲内容，无需添加其他任何额外信息或解释。"}
    ]
    print(f'[info] Generating the plot outline...')
    result = call_openai_api(api_config, messages, get_max_tokens(api_config['model']))
    # 扩写剧情大纲
    messages.append({"role": "assistant", "content": result})
    messages.append({"role": "user", "content": "请在保持Markdown格式不变的同时扩写剧情大纲的每一个部分，确保每个部分大于等于200字，且各个部分剧情发展速度合理，每一个部分都包含爽文剧情，且不能与上一个部分剧情存在重复。你可以根据需要引入新的人物、道具或地点等元素。请直接输出扩写后的剧情大纲，无需添加任何额外注释或说明。"})
    print(f'[info] Expanding the plot outline...')
    return call_openai_api(api_config, messages, get_max_tokens(api_config['model']))

# 生成章节概要
def generate_chapter_summaries(api_config, novel_config):
    messages = [
        {"role": "system", "content": "你是一位顶级网络文学创作顾问，参与过起点中文网等头部平台的爆款作品开发。熟悉各平台算法推荐机制、读者画像及商业化策略，擅长将市场趋势与文学性结合。"},
        {"role": "user", "content": f"我会先给你小说的相关信息，然后你再进行后面的工作。这本小说叫《{novel_config['novel_title']}》，约{round(novel_config['total_chapters'] * novel_config['words_per_chapter'] * 1.2)}字、共{novel_config['total_chapters']}章，类型是{novel_config['novel_genre']}。\n\n- 剧情简介：{novel_config['plot_summary_expand']}\n\n- 世界观：\n{novel_config['world_setting']}\n\n- 核心人物设定：\n{novel_config['character_settings']}"},
        {"role": "assistant", "content": "已收到，是否还有别的信息？"},
        {"role": "user", "content": f"以下是剧情大纲：{novel_config['plot_outline']}"},
        {"role": "assistant", "content": "已收到，可以开始工作。"},
    ]
    distribution = split_chapters(novel_config['total_chapters'], len(novel_config['plot_outline_json']['sections']))
    now_chapters = 1
    chapter_summaries = ""
    for index, chapters in enumerate(distribution):
        print(f'[info] Generating chapter summaries for Part{index + 1}...')
        messages.append({"role": "user", "content": f"请根据剧情大纲规划具体的章节，使用Markdown格式进行编写，每个章节都以二级标题（即“## ”开头）的形式单独列出，并紧跟这个章节的剧情概要（用200字简短概括，话语要精炼，可以根据需要引入新的人物、道具或地点等元素，适当添加爽文剧情），不要添加其他任何额外信息或解释。总共有{novel_config['total_chapters']}个章节，但现在你只需要先规划出“{novel_config['plot_outline_json']['titles'][index]}”这部分的{chapters}个章节（第{now_chapters}章到第{now_chapters + chapters - 1}章）每章的剧情概要，要与之前的章节保持剧情连贯。"})
        assistant_output = call_openai_api(api_config, messages, get_max_tokens(api_config['model']))
        assistant_output = assistant_output.replace('\n\n', '\n')
        messages.append({"role": "assistant", "content": assistant_output})
        now_chapters += chapters
        chapter_summaries += assistant_output + '\n\n'
    return chapter_summaries

# 生成章节内容
def generate_chapter_contents(global_config, novel_config):
    messages_static = [
        {"role": "system", "content": "你是一位顶级网络文学作者，拥有丰富的创作经验和深厚的文学功底，熟悉各大平台的算法推荐机制、读者画像以及商业化策略，并擅长将市场趋势与文学性完美结合。在进行创作时，请遵循以下要求：1.提高文本复杂程度。2.丰富词汇运用，使用多样化的词汇和表达方式，避免重复。3.增强内容不可预测性。4.优化文章节奏感，使得整个故事流畅自然。5.构建动态变化的句子结构，灵活变换句式长短。"},
        {"role": "user", "content": f"我会先给你小说的相关信息，然后你再开始具体的创作。这本小说叫《{novel_config['novel_title']}》。\n\n- 剧情简介：{novel_config['plot_summary_expand']}\n\n- 世界观：\n{novel_config['world_setting']}\n\n- 核心人物设定：\n{novel_config['character_settings']}"},
        {"role": "assistant", "content": "已收到，是否还有别的信息？"},
        # {"role": "user", "content": f"以下是剧情大纲：\n{novel_config['plot_outline']}"},
        # {"role": "assistant", "content": "已收到，是否还有别的信息？"},
        {"role": "user", "content": f"以下是各个章节的剧情梗概，请确保在创作时不超出对应章节的剧情范围：\n{novel_config['chapter_summaries']}"},
        {"role": "assistant", "content": "已收到，是否还有别的信息？"},
    ]
    
    chapter_contents = [] # 这里面储存生成好的章节
    for index, title in enumerate(novel_config['chapter_summaries_json']['titles']):
        print(f'[info] Generating specific content for Chapter {index + 1}...')

        # 跳过已生成的章节
        txt_output_path = os.path.join(global_config['file_paths']['output_directory'], "章节", f"{title}.txt")
        if os.path.exists(txt_output_path):
            print(f'[warning] Chapter {index + 1} already exists')
            chapter_contents.append(read_txt_to_string(txt_output_path)) # 从TXT里读取章节内容
            continue

        # 特殊提示词
        random_prompt = "，可根据情况融入爽点"
        if random.random() < 0.6: # 40%概率生效
            random_prompt = ""

        # 构建消息
        messages = []
        connector_prompt = ""
        if index != 0:
            messages.append({"role": "user", "content": f"以下是前几个章节的内容：\n{concatenate_last_n(chapter_contents, 3)}"}) # 提交前3个章节的内容
            messages.append({"role": "assistant", "content": "已收到，是否还有别的信息？"})
            connector_prompt = f"，剧情紧接第{index}章结尾“{get_last_20_chars(chapter_contents[-1])}”，且衔接处不能有重复或前情提要"
        messages.append({"role": "user", "content": f"没有了。请开始创作小说的第{index + 1}章{connector_prompt}，总字数{novel_config['words_per_chapter'] + 500}到{novel_config['words_per_chapter'] + 1000}字{random_prompt}。章节内容应按照给定的剧情梗概展开，并且在章节结尾处直接中断剧情，避免在结尾添加任何形式的总结、预示、暗示、伏笔、省略、“挑战开始”。请直接输出本章的具体内容，无需添加标题。以下是本章（{title}）的剧情梗概：{novel_config['chapter_summaries_json']['sections'][index]}"})
        new_messages = messages_static + messages

        assistant_output = call_openai_api_stream(global_config['api_config'], new_messages, get_max_tokens(global_config['api_config']['model']))
        chapter_contents.append(f"{novel_config['chapter_summaries_json']['titles'][index]}\n\n{assistant_output.replace('\n\n', '\n')}")
        write_string_to_txt(chapter_contents[-1], txt_output_path)
        break
    return chapter_contents

# 调用API
def call_openai_api(api_config, messages, max_tokens):
    client = OpenAI(api_key=api_config['api_key'], base_url=api_config['base_url'])
    temperature = 0.8
    if api_config['model'] == "deepseek-chat" or api_config['model'] == "deepseek-reasoner":
        temperature = 1.6
    try:
        completion = client.chat.completions.create( 
            model=api_config['model'], 
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        usage = {
            "completion_tokens": completion.usage.completion_tokens,
            "prompt_tokens": completion.usage.prompt_tokens,
            "total_tokens": completion.usage.total_tokens
        }
        update_usage_log(usage, api_config['base_url'], api_config['model'])
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[error] API connection failed: {e}")
        return None
    
def call_openai_api_stream(api_config, messages, max_tokens):
    client = OpenAI(api_key=api_config['api_key'], base_url=api_config['base_url'])
    temperature = 0.8
    if api_config['model'] == "deepseek-chat" or api_config['model'] == "deepseek-reasoner":
        temperature = 1.6
    try:
        response = client.chat.completions.create(
            model=api_config['model'],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True  # 启用流式传输
        )
        complete_response = ""
        last_chunk = None
        for chunk in response:
            last_chunk = chunk
            if hasattr(chunk.choices[0].delta, "content"):
                content_chunk = chunk.choices[0].delta.content
                print(content_chunk, end='', flush=True)
                complete_response += content_chunk
        print()
        usage = {
            "completion_tokens": last_chunk.usage.completion_tokens,
            "prompt_tokens": last_chunk.usage.prompt_tokens,
            "total_tokens": last_chunk.usage.total_tokens
        }
        update_usage_log(usage, api_config['base_url'], api_config['model'])
        return complete_response
    except Exception as e:
        print(f"[error] API connection failed: {e}")
        return None

if __name__ == '__main__':
    pass