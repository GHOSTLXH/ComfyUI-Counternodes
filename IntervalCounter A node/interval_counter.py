import os
import json

class IntervalCounter:
    SAVE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "interval_counter_state.json")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reset": ("BOOLEAN", {"default": False}),
                "mode": (["increment", "decrement", "inc_to_max", "dec_to_min"], {"default": "increment"}),
                "min_value": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "max_value": ("INT", {"default": 100, "min": 0, "max": 10000}),
                "step": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "trigger_interval": ("INT", {"default": 3, "min": 1, "max": 10000}),
                "tick": ("INT", {"default": 0, "min": 0, "max": 999999}),  # 新增的 "tick" 输入，用于接收计数器节点的输出
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "counter"
    CATEGORY = "Custom Nodes/Counters"

 # Set IS_CHANGED to True to ensure the node is always considered dirty
    IS_CHANGED = True
    
    def __init__(self):
        self.load_state()

    def counter(self, reset, mode, min_value, max_value, step, trigger_interval, tick):
        print(f"Before: _current_interval_count={self._current_interval_count}, trigger_interval={trigger_interval}, mode={mode}, value={self.value}, reset={reset}, tick={tick}")
        if reset:
            self.reset_state(min_value)
        else:
            if self.current_mode != mode:
                self.current_mode = mode
                self._current_interval_count = 0

            self._current_interval_count += 1

            if self._current_interval_count >= trigger_interval:
                self._current_interval_count = 0
                if self.current_mode == "increment":
                    self.value = min(self.value + step, max_value)
                elif self.current_mode == "decrement":
                    self.value = max(self.value - step, min_value)
                elif self.current_mode == "inc_to_max":
                    self.value = max_value
                elif self.current_mode == "dec_to_min":
                    self.value = min_value
        print(f"After: _current_interval_count={self._current_interval_count}, trigger_interval={trigger_interval}, mode={mode}, value={self.value}")
        self.save_state()
        return (self.value,)

    def load_state(self):
        try:
            with open(self.SAVE_FILE, 'r') as f:
                state = json.load(f)
                self.value = state.get("value", 0)
                self._current_interval_count = state.get("interval_count", 0)
                self.current_mode = state.get("mode", "increment")
                print(f"Loaded state: {state}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.reset_state()
            print(f"State file not found or invalid. Resetting state.")

    def save_state(self):
        state = {
            "value": self.value,
            "interval_count": self._current_interval_count,
            "mode": self.current_mode
        }
        with open(self.SAVE_FILE, 'w') as f:
            json.dump(state, f)
        print(f"Saved state: {state}")

    def reset_state(self, min_value=0):
        self.value = min_value
        self._current_interval_count = 0
        self.current_mode = "increment"
        self.save_state()

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "IntervalCounter": IntervalCounter
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "IntervalCounter": "Interval Counter"
}
