import string
from random import SystemRandom
from django.utils.text import slugify

def random_letters(k):
    return "".join(SystemRandom().choices(
        string.ascii_lowercase + string.digits, k=k
    ))


def slugify_new(text: str, k=5):
    return slugify(text) +  "-" + random_letters(k)


print(slugify_new('Este blog falaremos sobre'))