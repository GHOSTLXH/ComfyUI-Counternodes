# __init__.py

from .AlternatingOutputB import AlternatingOutputB

NODE_CLASS_MAPPINGS = {
    "AlternatingOutputB": AlternatingOutputB,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AlternatingOutputB": "Alternating Output B",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
