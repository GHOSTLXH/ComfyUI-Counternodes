from .interval_counter import IntervalCounter

NODE_CLASS_MAPPINGS = {
    "IntervalCounter": IntervalCounter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IntervalCounter": "Interval Counter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
