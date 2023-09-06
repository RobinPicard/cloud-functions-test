import logging
import os
from typing import List, Tuple


class CustomLogger:
    """Logger class to conveniently log colored and centered messages"""
    COLORS = {
        'RED': '\033[31m',
        'GREEN': '\033[92m',
        'CYAN': '\033[96m',
        'DEFAULT': '\033[0m',
    }

    def __init__(self, name: str) -> None:
        """Create the logger object and modify the format to keep only the message"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log_colored(self, messages: List[Tuple[str, str]]) -> None:
        """Log the messages provided with their respective color on one line"""
        if not messages:
            return
        # if we receive a single item, put it in a list
        if not isinstance(messages, list):
            messages = [messages]
        # make sure each each item of the list is a tuple
        for i, item in enumerate(messages):
            if not isinstance(item, tuple):
                messages[i] = (item, "DEFAULT")
            elif len(item) == 1:
                messages[i] = (item[0], "DEFAULT")
        display_message = ''
        for content, color in messages:
            display_message += f"{self.COLORS.get(color.upper(), '')}{content}{self.COLORS['DEFAULT']}"
        self.logger.info(display_message)

    def log_centered(self, messages: List[str], padding_char: str = '=') -> None:
        """Log the messages provided in the center of the terminal with the padding_chars all around it"""
        display_message = ' ' + "".join(messages) + ' '
        term_width = os.get_terminal_size().columns
        padding_needed = term_width - len(display_message)
        padding_one_side = padding_needed // 2
        padded_string = padding_char * padding_one_side + display_message + padding_char * padding_one_side
        if padding_needed % 2 != 0:
            padded_string += padding_char
        self.logger.info(padded_string)


custom_logger = CustomLogger('custom_logger')
