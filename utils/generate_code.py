from django.utils.crypto import get_random_string


def get_random_key(length=50):
    return get_random_string(length=length)
