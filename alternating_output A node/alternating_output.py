import torch

class AlternatingOutput:
    """
    每 n 轮输出一次 input_a 的图像，其余时间输出 input_b 的图像。
    只处理 IMAGE 类型输入。
    添加了输出图像宽度和高度的整数输出端口。
    添加了 first_output 选项，允许用户选择第一次输出的图像。
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_a": (
                    "IMAGE",
                    {"forceInput": True},
                ),
                "input_b": (
                    "IMAGE",
                    {"forceInput": True},
                ),
                "n": ("INT", {"default": 5, "min": 1, "max": 10000}),
                "first_output": (["input_a", "input_b"], {"default": "input_a"}),
                "counter": ("INT", {"default": 0, "min": 0, "max": 10000}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height", "counter")
    OUTPUT_NODE = True
    FUNCTION = "alternate"
    CATEGORY = "Utils"

 # Set IS_CHANGED to True to ensure the node is always considered dirty
    IS_CHANGED = True
    
    def alternate(self, input_a, input_b, n, first_output, counter):
        # 检查和处理 input_a
        if torch.is_tensor(input_a) and input_a.ndim == 4:
            image_a = input_a
        elif isinstance(input_a, tuple) and len(input_a) > 0 and torch.is_tensor(input_a[0]) and input_a[0].ndim == 4:
            image_a = input_a[0]
            print(f"[AlternatingOutput] WARNING: input_a is a tuple. Extracting the first element as the IMAGE tensor.")
        else:
            raise ValueError(f"[AlternatingOutput] ERROR: input_a is not an IMAGE tensor or a valid tuple. Received type: {type(input_a)}")

        # 检查和处理 input_b
        if torch.is_tensor(input_b) and input_b.ndim == 4:
            image_b = input_b
        elif isinstance(input_b, tuple) and len(input_b) > 0 and torch.is_tensor(input_b[0]) and input_b[0].ndim == 4:
            image_b = input_b[0]
            print(f"[AlternatingOutput] WARNING: input_b is a tuple. Extracting the first element as the IMAGE tensor.")
        else:
            raise ValueError(f"[AlternatingOutput] ERROR: input_b is not an IMAGE tensor or a valid tuple. Received type: {type(input_b)}")

        # 根据 first_output 和 counter 决定输出哪个图像
        if counter == 0:  # 第一次执行
            if first_output == "input_a":
                output = image_a
            else:
                output = image_b
        elif counter % n == 0:
            output = image_a
        else:
            output = image_b

        # 获取图像的宽度和高度
        _, height, width, _ = output.shape

        # 递增 counter
        counter += 1

        return (output, width, height, counter)
