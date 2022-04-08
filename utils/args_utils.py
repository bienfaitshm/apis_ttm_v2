
def kwargs_id_creator(**kwargs) -> dict:
    tmp = {}
    for _key, value in kwargs.items():
        tmp_name = f"{_key}_id" if isinstance(value, int) else _key
        tmp[tmp_name] = value
    return tmp
