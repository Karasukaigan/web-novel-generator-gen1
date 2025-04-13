import sys
from src.tools import *
from src.core import *

if __name__ == '__main__':
    # 加载全局配置
    global_config = read_json_to_dict('global_config.json')
    api_config = global_config['api_config']
    print(f"[info] base_url: {api_config['base_url']}")
    print(f"[info] model: {api_config['model']}")
    input_directory = global_config['file_paths']['input_directory']
    output_directory = global_config['file_paths']['output_directory']
    print(f"[info] input_directory: {input_directory}")
    print(f"[info] output_directory: {output_directory}")

    # 测试API配置是否正确
    api_connection = test_api_connection(api_config['base_url'], api_config['api_key'], api_config['model'])
    if not api_connection:
        sys.exit(1)

    # 加载小说配置
    novel_config_path = os.path.join(input_directory, 'novel_config.json')
    novel_config = read_json_to_dict(novel_config_path)
    if not validate_novel_config(novel_config):
        sys.exit(1)
    if not novel_config.get('novel_title'):
        novel_config['novel_title'] = generate_novel_title(api_config, novel_config['plot_summary']) # 如果没有小说名则生成一个
        write_dict_to_json(novel_config, novel_config_path)
    print(f"[info] novel_title: {novel_config['novel_title']}")
    if not novel_config.get('novel_genre'):
        novel_config['novel_genre'] = determine_novel_genre(api_config, novel_config['plot_summary']) # 如果没有小说类型则自动判断
        write_dict_to_json(novel_config, novel_config_path)
    print(f"[info] novel_genre: {novel_config['novel_genre']}")
    print(f"[info] plot_summary: {summarize_text(novel_config['plot_summary'])}")
    print(f"[info] total_chapters: {novel_config['total_chapters']}")
    print(f"[info] words_per_chapter: {novel_config['words_per_chapter']}")

    # 扩展剧情简介
    if not novel_config.get('plot_summary_expand'):
        novel_config['plot_summary_expand'] = expand_plot_summary(api_config, novel_config['plot_summary'])
        write_dict_to_json(novel_config, novel_config_path)
    print(f"[info] plot_summary_expand: {summarize_text(novel_config['plot_summary_expand'])}")
    plot_summary_path = os.path.join(output_directory, '剧情简介.md')
    if not os.path.exists(plot_summary_path):
        write_string_to_txt(f"# {novel_config['novel_title']}\n\n{novel_config['plot_summary_expand']}", plot_summary_path)

    # 润色剧情简介
    if not novel_config.get('plot_summary_refined'):
        novel_config['plot_summary_refined'] = refine_plot_summary(api_config, novel_config['plot_summary_expand'])
        write_dict_to_json(novel_config, novel_config_path)
    print(f"[info] plot_summary_refined: {summarize_text(novel_config['plot_summary_refined'])}")

    # 生成世界观
    if not novel_config.get('world_setting'):
        novel_config['world_setting'] = generate_world_setting(api_config, novel_config)
        write_dict_to_json(novel_config, novel_config_path)
    world_setting_path = os.path.join(output_directory, '世界观设定.md')
    if not os.path.exists(world_setting_path):
        write_string_to_txt(novel_config['world_setting'], world_setting_path)

    # 生成角色设定
    if not novel_config.get('character_settings'):
        novel_config['character_settings'] = generate_character_settings(api_config, novel_config)
        write_dict_to_json(novel_config, novel_config_path)
    character_settings_path = os.path.join(output_directory, '角色设定.md')
    if not os.path.exists(character_settings_path):
        write_string_to_txt(novel_config['character_settings'], character_settings_path)

    # 生成剧情大纲
    if not novel_config.get('plot_outline'):
        plot_outline = generate_plot_outline(api_config, novel_config)
        novel_config['plot_outline'] = plot_outline
        novel_config['plot_outline_json'] = extract_sections(plot_outline)
        write_dict_to_json(novel_config, novel_config_path)
        # 输出为TXT文件
        plot_outline_path = os.path.join(output_directory, '剧情大纲.md')
        write_string_to_txt(plot_outline, plot_outline_path)
    for index, section in enumerate(novel_config['plot_outline_json']['sections']):
        print(f"[info] {novel_config['plot_outline_json']['titles'][index]}: {summarize_text(novel_config['plot_outline_json']['sections'][index])}")
    
    # 生成章节概要
    if not novel_config.get('chapter_summaries'):
        chapter_summaries = generate_chapter_summaries(api_config, novel_config)
        chapter_summaries = chapter_summaries.replace('\n\n', '\n').replace('\n\n', '\n').replace('\n#', '\n\n#')
        novel_config['chapter_summaries'] = chapter_summaries
        novel_config['chapter_summaries_json'] = extract_sections(chapter_summaries)
        write_dict_to_json(novel_config, novel_config_path)
        # 输出为TXT文件
        chapter_summaries_path = os.path.join(output_directory, '章节概要.md')
        write_string_to_txt(chapter_summaries, chapter_summaries_path)
    for index, section in enumerate(novel_config['chapter_summaries_json']['sections']):
        print(f"[info] {novel_config['chapter_summaries_json']['titles'][index]}: {summarize_text(novel_config['chapter_summaries_json']['sections'][index])}")

    # 生成具体章节
    chapter_contents = generate_chapter_contents(global_config, novel_config)
    if not novel_config.get('chapter_contents'):
        novel_config['chapter_contents'] = chapter_contents

    # 合并所有章节
    txt_content = f"《{novel_config['novel_title']}》\n简介：{novel_config['plot_summary_refined']}\n\n"
    for index, title in enumerate(novel_config['chapter_summaries_json']['titles']):
        if os.path.exists(os.path.join(global_config['file_paths']['output_directory'], "章节", f"{title}.txt")):
            txt_content += f"{read_txt_to_string(os.path.join(global_config['file_paths']['output_directory'], "章节", f"{title}.txt"))}\n\n\n"
    write_string_to_txt(txt_content, os.path.join(global_config['file_paths']['output_directory'], f"{novel_config['novel_title']}.txt"))