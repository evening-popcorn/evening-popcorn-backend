import random
import string


def generate_random_string(length: int) -> str:
    """
    Generate random string of characters
    Used for generating tokens
    """
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))
