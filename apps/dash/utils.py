
def get_routes_to_string(routes):
    names_tuple = []
    # for i in routes:
    #     _from = i.route.whereFrom.town
    #     _to = i.route.whreTo.town
    #     if _from not in names_tuple:
    #         names_tuple.append(_from)
    #     if _to not in names_tuple:
    #         names_tuple.append(_to)
    return " -> ".join(names_tuple)