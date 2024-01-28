import string
import random


def generate(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
