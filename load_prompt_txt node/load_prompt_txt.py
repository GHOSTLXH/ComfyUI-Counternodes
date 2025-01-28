import os
import re

class LoadPromptFromTXT:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": "C:\\"}),  # Directory path
                "index": ("INT", {"default": 0, "min": 0, "max": 10000}), # Index value
                "trigger": ("INT", {"default": 0, "min": 0, "max": 9999999999})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "load_prompt"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def natural_sort_key(self, s):
        """
        Generates a key for natural sorting.
        """
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(r'(\d+)', s)]

    def load_prompt(self, directory, index, trigger):
        image_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))]
        image_files = sorted(image_files, key=self.natural_sort_key)

        if not 0 <= index < len(image_files):
            print(f"Warning: Index {index} out of range for directory {directory}. Returning empty prompt.")
            return ("",)

        # **关键修改: 使用 index 选择图像文件名**
        img_filename = os.path.splitext(image_files[index])[0]
        txt_path = os.path.join(directory, f"{img_filename}.txt")

        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
            print(f"Loaded prompt from: {txt_path} with index: {index}")
        except FileNotFoundError:
            prompt = ""
            print(f"Warning: TXT file not found: {txt_path}. Returning empty prompt.")

        return (prompt,)

NODE_CLASS_MAPPINGS = {
    "LoadPromptFromTXT": LoadPromptFromTXT
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadPromptFromTXT": "Load Prompt from TXT"
}