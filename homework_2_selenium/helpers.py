import random
import string
import time


def random_string(
        size: int = 10,
        chars=string.ascii_uppercase + string.ascii_lowercase + string.digits,
) -> str:
    return "".join(random.choice(chars) for _ in range(size))


def random_email():
    return f"{random_string()}@{random_string(size=random.randint(2, 4))}." \
           f"{random.choice(['ru', 'com', 'net', 'kz', 'co'])}"


class TimeoutException(Exception):
    pass


def wait_until_success(method, error=Exception, timeout=10, interval=0.5, check=False, **kwargs):
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
