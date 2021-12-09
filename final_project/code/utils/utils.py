import random
import string
import time


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


def check_contain_in_list(pattern: str, array: list) -> bool:
    for elem in array:
        if pattern in elem:
            return True
    return False
