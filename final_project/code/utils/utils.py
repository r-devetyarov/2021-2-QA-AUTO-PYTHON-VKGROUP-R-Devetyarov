import random
import string
import subprocess
import time

from datetime import datetime


class TimeoutException(Exception):
    pass


def wait(method, error=Exception, timeout=10, interval=0.5, check=False, **kwargs):
    started = time.time()
    last_exception = None
    while time.time() - started < timeout:
        try:
            result = method(**kwargs)
            if check:
                if result:
                    return result
                last_exception = f'Method {method.__name__} returned {result}'
            else:
                return result
        except error as e:
            last_exception = e

        time.sleep(interval)

    raise TimeoutException(f'Method {method.__name__} timeout out in {timeout}sec with exception: {last_exception}')


def random_string(
        size: int = 10,
        chars=string.ascii_uppercase + string.ascii_lowercase + string.digits,
) -> str:
    return "".join(random.choice(chars) for _ in range(size))


def random_email(size: int = 10):
    str_size = size - 4
    return f"{random_string(size=str_size)}@a.a"


def check_contain_in_list(pattern: str, array: list) -> bool:
    for elem in array:
        if pattern in elem:
            return True
    return False


def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')


def run_command(cmd):
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
