import os
import json

class ImageCounter:
    SAVE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image_counter_state.json")

    def __init__(self):
        self.load_state()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "reset": ("BOOLEAN", {"default": False}),
                "increment": ("INT", {"default": 1, "min": 1, "max": 100}),
                "trigger_interval": ("INT", {"default": 1, "min": 1, "max": 10000}),  # 添加 trigger_interval
            },
            "optional": {
                "trigger": ("*",)
            }
        }

    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("image", "count")
    FUNCTION = "count_image"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def count_image(self, image, reset, increment, trigger_interval, trigger=None):
        print(f"Before: count={self.count}, _current_interval_count={self._current_interval_count}, trigger_interval={trigger_interval}, reset={reset}")
        if reset:
            self.reset_state()
        else:
            self._current_interval_count += 1
            if self._current_interval_count >= trigger_interval:
                self.count += increment
                self._current_interval_count = 0

        print(f"After: count={self.count}, _current_interval_count={self._current_interval_count}")
        self.save_state()
        return (image, self.count)

    def load_state(self):
        try:
            with open(self.SAVE_FILE, 'r') as f:
                state = json.load(f)
                self.count = state.get("count", 0)
                self._current_interval_count = state.get("interval_count", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.reset_state()

    def save_state(self):
        state = {
            "count": self.count,
            "interval_count": self._current_interval_count
        }
        with open(self.SAVE_FILE, 'w') as f:
            json.dump(state, f)

    def reset_state(self):
        self.count = 0
        self._current_interval_count = 0
        self.save_state()

# 一个包含所有你想要导出的节点及其名称的字典
# 注意：名称应该是全局唯一的
NODE_CLASS_MAPPINGS = {
    "ImageCounter": ImageCounter
}

# 一个包含节点友好/人类可读标题的字典
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCounter": "Interval Image Counter"
}