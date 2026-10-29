import re
import random

class CustomWildcardPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "A man in {blue jeans|shorts|swim trunks} standing on a {wood|concrete} board"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("final_prompt", "debug_info")
    FUNCTION = "process_wildcards"
    CATEGORY = "utils/custom"

    def process_wildcards(self, text, seed):
        # Перевірка на дужки
        open_brackets = text.count("{")
        close_brackets = text.count("}")
        
        if open_brackets != close_brackets:
            error_msg = f"!!! SYNTAX ERROR: {open_brackets} open vs {close_brackets} closed brackets !!!"
            return (text, error_msg)

        # Використовуємо локальний екземпляр Random, щоб не збивати глобальний стан
        gen = random.Random(seed)
        
        selected_list = []
        
        def replace_choice(match):
            # Прибираємо дужки та розділяємо варіанти
            content = match.group(1)
            options = [opt.strip() for opt in content.split("|") if opt.strip()]
            
            if not options:
                return ""
                
            choice = gen.choice(options)
            selected_list.append(choice)
            return choice

        # Регулярка шукає найменші внутрішні блоки { }
        # Це дозволяє уникати помилок, якщо в тексті є звичайні дужки ( )
        pattern = r"\{([^{}]+)\}"
        
        # Робимо заміну
        result_prompt = re.sub(pattern, replace_choice, text)
        
        # Формуємо звіт для підсвічування
        debug_str = " | ".join(selected_list) if selected_list else "No choices made"
        
        return (result_prompt, f"✅ Selected: {debug_str}")

NODE_CLASS_MAPPINGS = {"CustomWildcardPrompt": CustomWildcardPrompt}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomWildcardPrompt": "🛠️ Custom Wildcard Prompt"}
