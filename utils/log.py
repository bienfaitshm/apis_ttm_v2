import json


def log(v):
    print(json.dumps(v, indent=2, default=str))
