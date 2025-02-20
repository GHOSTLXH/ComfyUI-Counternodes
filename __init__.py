# __init__.py
from .alternating_output import AlternatingOutput
from .AlternatingOutputB import AlternatingOutputB
from .image_counter import ImageCounter
from .interval_counter import IntervalCounter
from .interval_counter_b import IntervalCounterB
from .load_prompt_txt import LoadPromptFromTXT

NODE_CLASS_MAPPINGS = {
    "AlternatingOutput": AlternatingOutput,
    "AlternatingOutputB": AlternatingOutputB,
    "ImageCounter": ImageCounter,
    "IntervalCounter": IntervalCounter,
    "IntervalCounterB": IntervalCounterB,
    "LoadPromptFromTXT": LoadPromptFromTXT,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AlternatingOutput": "Alternating Output",
    "AlternatingOutputB": "Alternating Output B",
    "ImageCounter": "Interval Image Counter",
    "IntervalCounter": "Interval Counter",
    "IntervalCounterB": "Interval Counter B",
    "LoadPromptFromTXT": "Load Prompt from TXT",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']