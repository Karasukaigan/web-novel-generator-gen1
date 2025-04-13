# 返回模型对应的max_tokens
def get_max_tokens(model_name):
    model_max_tokens = {
        # 阿里云百炼
        "qwen-max": 8192,
        "qwen-max-latest": 8192,
        "qwen-plus": 8192,
        "qwen-plus-latest": 8192,
        "qwen-turbo": 8192,
        "qwen-turbo-latest": 8192,
        "qwen-long": 6000,
        "qwq-plus": 8192,
        "qwq-plus-latest": 8192,
        
        # DeepSeek
        "deepseek-chat": 8000,
        "deepseek-reasoner": 8000,

        # SiliconFlow
        "deepseek-ai/DeepSeek-R1": 16384,
        "Pro/deepseek-ai/DeepSeek-R1": 16384,
        "deepseek-ai/DeepSeek-V3": 4096,
        "Pro/deepseek-ai/DeepSeek-V3": 4096,
        "Qwen/QwQ-32B-Preview": 8192,
        
        # OpenAI
        "gpt-4": 8192,
        "o1": 100000,
        "gpt-4-turbo": 4096,
        "gpt-4o": 16384,
        "o1-mini": 65536,
        "o3-mini": 100000,
        "gpt-4o": 16384,
        "gpt-3.5-turbo": 4096,
        "gpt-4o-mini": 16384,

        # Anthropic
        "claude-3-7-sonnet-20250219": 8192,
        "claude-3-5-sonnet-20241022": 8192,
        "claude-3-5-haiku-20241022": 8192,
    }
    if model_name in model_max_tokens:
        return model_max_tokens[model_name]
    else:
        return 2000
    
if __name__ == '__main__':
    print(get_max_tokens("deepseek-chat"))