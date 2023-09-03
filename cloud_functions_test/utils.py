import fcntl
import os
from math import floor
from typing import Tuple


def log_reader(process: object) -> Tuple[str, str]:
    """Read all available logs and return them in a tuple(error, standard)"""
    standard_logs = []
    error_logs = []
    while True:
        line = process.stdout.readline()
        if line:
            new_logs.append(line.decode('utf-8'))
        else:
            break
    while True:
        line = process.stderr.readline()
        if line:
            line = line.decode('utf-8')
            # logging.error/warning are added to stderr but we want to treat them as standard logs
            if line.startswith('ERROR:') or line.startswith('WARNING:'):
                standard_logs.append(line)
            else:
                error_logs.append(line)
        else:
            break
    return(
        "".join(error_logs).strip('\n'),
        "".join(standard_logs).strip('\n')
    )


def set_fd_nonblocking(fd: object) -> None:
    """Set file descriptor to non-blocking such that we can read the logs without blocking the thread"""
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def print_centered_text(text: str, padding_char: str = '=') -> None:
    """Print text provided in the center of the terminal with the padding_chars all around it"""
    text = ' ' + text + ' '
    term_width = os.get_terminal_size().columns
    padding_needed = term_width - len(text)
    padding_one_side = padding_needed // 2
    padded_string = padding_char * padding_one_side + text + padding_char * padding_one_side
    if padding_needed % 2 != 0:
        padded_string += padding_char
    print(padded_string)
