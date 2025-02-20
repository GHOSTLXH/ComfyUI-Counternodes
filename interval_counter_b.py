import os
import json
import ast
import operator

class IntervalCounterB:
    SAVE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "interval_counter_b_state.json")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reset": ("BOOLEAN", {"default": False}),
                "mode": (["increment", "decrement", "inc_to_max", "dec_to_min", "expression"], {"default": "increment"}),
                "min_value": ("INT", {"default": 0, "min": -10000, "max": 10000}),
                "max_value": ("INT", {"default": 100, "min": -10000, "max": 10000}),
                "step": ("INT", {"default": 1, "min": 1, "max": 10000}),
                "trigger_interval": ("INT", {"default": 3, "min": 1, "max": 10000}),
                "tick": ("INT", {"default": 0, "min": 0, "max": 999999}),
                "expression": ("STRING", {"default": "value + 1"}),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "counter"
    CATEGORY = "Custom Nodes/Counters"

    def __init__(self):
        self.load_state()

    def _safe_eval_expression(self, expression, value):
        # 定义允许的操作符
        operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod
        }
        
        # 将表达式转换为标准格式
        expression = expression.replace('value', str(value))
        
        try:
            # 尝试直接作为数学表达式计算
            return ast.literal_eval(expression)
        except (ValueError, SyntaxError):
            # 如果不是简单表达式，进行基本运算符解析
            for op, func in operators.items():
                if op in expression:
                    parts = expression.split(op)
                    if len(parts) == 2:
                        try:
                            left = ast.literal_eval(parts[0].strip())
                            right = ast.literal_eval(parts[1].strip())
                            return func(left, right)
                        except (ValueError, SyntaxError):
                            continue
            raise ValueError("不支持的表达式格式")

    def counter(self, reset, mode, min_value, max_value, step, trigger_interval, tick, expression):
        # 确保trigger_interval是整数
        trigger_interval = int(trigger_interval)
        
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
                elif self.current_mode == "expression":
                    try:
                        # 使用安全的表达式计算方法
                        self.value = self._safe_eval_expression(expression, self.value)
                        self.value = max(min(self.value, max_value), min_value)  # Clamp the value
                    except Exception as e:
                        print(f"Error evaluating expression: {e}")
        self.save_state()
        return (int(self.value),)

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

NODE_CLASS_MAPPINGS = {
    "IntervalCounterB": IntervalCounterB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IntervalCounterB": "Interval Counter B"
}