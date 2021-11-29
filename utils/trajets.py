import json
from typing import Any


def log(v):
    print(json.dumps(v, indent=2, default=str))

def create_trajet_object(values, value, p=None, n=None):
    """
        creation of object linked traject
    """
    values[value.pk] = {
        'prev':p,
        'next':n,
        'data': value
    }

def get_init(routes :dict, init :str = "init"):
    """ return the first cover or the last"""
    v = 'prev' if init == 'init' else 'next'
    for value in routes.values():
        if value.get(v) is None :
            return value

def link_routes (routes):
    _routes = {}
    for i, item in enumerate(routes):
        a = item.whereTo
        b = item.whereFrom
        if i < 1:
            create_trajet_object(_routes, a, p = b)
            create_trajet_object(_routes, b, n = a)
        else :

            if a.pk in _routes:
                _routes[a.pk]['prev'] = b
            else:
                create_trajet_object(_routes, a, p = b)
            
            if b.pk in _routes:
                _routes[b.pk]['next'] = a
            else:
                create_trajet_object(_routes, b, n = a)
    return _routes

def tracer(routes, init):
    d = []
    if not init:
        return d
    nex_object = init.get('next')
    d +=[init.get('data')]
    if nex_object:
        data = routes.get(nex_object.pk)
        return d + tracer(routes, data)
    return d

def count_init(routes :dict) -> tuple[int, int]:
    n_next = 0
    n_prev = 0

    for i in routes.values():
        if not i.get('next'):
            n_next += 1
        if not i.get('prev'):
            n_prev += 1
    return n_prev, n_next

def is_valide_routing(routes:dict):
    """ check if the route has the end and the start"""
    p,n = count_init(routes)
    return n == 1 and p == 1

def get_routes(routes):
    init = get_init(routes)
    if not is_valide_routing(routes):
        return []
    return tracer(routes, init)

def make_trajet(v):
    d = []
    for i, value in enumerate(v):
        d.append({
            'value': i,
            'label':value.town
        })
    return d
