# 网络小说生成器一代（Web Novel Generator Generation 1）

这是一个实验性项目，基于大语言模型打造的网络小说自动创作工具。项目采用“先总后分”的创作策略，通过模块化设计，实现从世界观构建到章节细化的完整创作流程自动化。

`代码修仙.txt`是使用本项目生成的小说，您可以查看它来了解最终的生成质量。

## 核心特性

- **小说命名**：根据小说简介，自动生成符合网文风格的书名。
- **世界观构建**：生成多维度、层次丰富的世界设定。
- **角色设定生成**：结合篇幅与世界观，自动生成主要角色设定。
- **大纲生成**：输出完整剧情大纲，涵盖起承转合。
- **章节生成**：基于上下文进行渐进式内容生成，保证剧情自然流畅。
- **双阶段创作架构**：“总-分”结构，先搭建宏观框架，再逐步填充细节。
- **流式输出支持**：支持实时内容生成，可随时中断和调整。

## 严正声明

本项目**仅用于从技术角度探讨人工智能生成网络小说的可行性与实现机制**，其目的在于研究自然语言处理与自动化创作系统的潜力与局限性。**本项目并不倡导、鼓励或支持使用人工智能进行小说创作，更明确禁止任何形式的滥用行为。**

请勿将本项目用于以下用途，包括但不限于：

- 批量生成、发布或销售由AI生成的小说内容；
- 用于侵犯他人版权、抄袭、误导性内容生产等不当行为；
- 以任何形式将本项目用于商业化目的。

任何使用者应自行承担因使用本项目产生的一切后果。项目作者不对由此引发的任何法律、道德或经济问题承担责任。

## 快速开始

### 前置要求

- 下载并安装 [Python](https://www.python.org/downloads/)
- 下载并安装 [Git](https://git-scm.com/downloads)
- 获取 [DeepSeek API Key](https://www.deepseek.com/)

### 步骤指南

1. **克隆项目到本地**
    ```
    git clone https://github.com/Karasukaigan/web-novel-generator-gen1.git
    ```

2. **安装OpenAI库**
    ```
    pip install openai
    ```

3. **配置全局设置（global_config.json）**  
    去掉`global_config.json.example`的`.example`后缀，然后编辑`global_config.json`，在`api_key`里填写您真实的API Key：  
    ```
    {
        "file_paths": {
            "input_directory": "input",
            "output_directory": "output"
        },
        "api_config": {
            "base_url": "https://api.deepseek.com/v1",
            "api_key": "your_api_key_here",
            "model": "deepseek-chat"
        }
    }
    ```
    得益于OpenAI库的通用性，可通过修改`base_url`来适配不同平台的API，例如阿里云百炼、硅基流动等。

4. **配置小说设置（novel_config.json）**
    去掉`input/novel_config.json.example`的`.example`后缀，然后编辑`novel_config.json`，例如： 
    ```
    {
        "novel_title": "代码修仙",
        "novel_genre": "玄幻",
        "plot_summary": "计算机系毕业生李凡在现实世界屡屡碰壁，无奈成为外卖员。一次送餐途中遭遇车祸，意外穿越到玄幻世界，成为小宗门的外门弟子。天赋平平的他被分配打扫藏书阁，却因一次偶然翻看阵法书籍，发现阵法原理竟与编程逻辑惊人相似。凭借扎实的计算机功底，李凡迅速掌握阵法精髓，并创新出前所未有的强大阵法。从此，他以“阵法程序员”的身份逆天改命，踏上了一条与众不同的修仙之路。",
        "total_chapters": 100,
        "words_per_chapter": 2000
    }
    ```

5. **开始生成**
    ```
    python run.py
    ```
    您可以在`output`目录里查看生成好的文件。

## 主要文件

- **run.py：** 主程序入口
- **global_config.json：** 全局配置文件
- **input/novel_config.json：** 小说配置文件
- **src/core.py：** 实现小说生成的核心模块，包含提示词。
