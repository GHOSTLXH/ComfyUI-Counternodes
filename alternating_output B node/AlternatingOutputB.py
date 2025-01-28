import torch

class AlternatingOutputB:
    """
    Implements a custom alternating output pattern:
    - If first_output is "input_a": Outputs A, B, B, ..., B, A, B, B, ..., B, A, ... (A, then n-1 times B, then A, and repeat)
    - If first_output is "input_b": Outputs B, A, A, ..., A, B, A, A, ..., A, B, ... (B, then n-1 times A, then B, and repeat)
    Handles only IMAGE type input.
    Adds integer output ports for image width and height.
    Adds a first_output option to select the first image to output.
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
                "n": ("INT", {"default": 3, "min": 2, "max": 10000}), # n should be at least 2
                "first_output": (["input_a", "input_b"], {"default": "input_a"}),
                "counter": ("INT", {"default": 0, "min": 0, "max": 10000}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height", "counter")
    OUTPUT_NODE = True
    FUNCTION = "alternate"
    CATEGORY = "Utils"

    def alternate(self, input_a, input_b, n, first_output, counter):
        # 检查和处理 input_a
        if torch.is_tensor(input_a) and input_a.ndim == 4:
            image_a = input_a
        elif isinstance(input_a, tuple) and len(input_a) > 0 and torch.is_tensor(input_a[0]) and input_a[0].ndim == 4:
            image_a = input_a[0]
            print(f"[AlternatingOutputB] WARNING: input_a is a tuple. Extracting the first element as the IMAGE tensor.")
        else:
            raise ValueError(f"[AlternatingOutputB] ERROR: input_a is not an IMAGE tensor or a valid tuple. Received type: {type(input_a)}")

        # 检查和处理 input_b
        if torch.is_tensor(input_b) and input_b.ndim == 4:
            image_b = input_b
        elif isinstance(input_b, tuple) and len(input_b) > 0 and torch.is_tensor(input_b[0]) and input_b[0].ndim == 4:
            image_b = input_b[0]
            print(f"[AlternatingOutputB] WARNING: input_b is a tuple. Extracting the first element as the IMAGE tensor.")
        else:
            raise ValueError(f"[AlternatingOutputB] ERROR: input_b is not an IMAGE tensor or a valid tuple. Received type: {type(input_b)}")

        # 根据 first_output 和 counter 决定输出哪个图像
        if counter == 0:
            output = image_a if first_output == "input_a" else image_b
        else:
            cycle_position = (counter - 1) % n
            if first_output == "input_a":
                if cycle_position == 0:
                  output = image_a
                else:
                  output = image_b
            else: # first_output == "input_b"
                if cycle_position == 0:
                  output = image_b
                else:
                  output = image_a

        # 获取图像的宽度和高度
        _, height, width, _ = output.shape

        # 递增 counter
        counter += 1

        return (output, width, height, counter)