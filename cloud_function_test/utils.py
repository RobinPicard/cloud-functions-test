import fcntl
import os
from math import floor


def log_reader(all_logs) -> str:
    """Read logs and return them as a single string."""
    new_logs = []
    while True:
        line = all_logs.readline()
        if line:
            new_logs.append(line.decode('utf-8'))
        else:
            break
    return "".join(new_logs).strip('\n')


def set_fd_nonblocking(fd):
    """Set file descriptor to non-blocking (Unix)."""
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def print_centered_text(text, padding_char='='):
    """Print text centered in the terminal."""
    term_width = os.get_terminal_size().columns

    text = ' ' + text + ' '

    padding_needed = term_width - len(text)
    padding_one_side = padding_needed // 2

    padded_string = padding_char * padding_one_side + text + padding_char * padding_one_side

    if padding_needed % 2 != 0:
        padded_string += padding_char

    print(padded_string)
