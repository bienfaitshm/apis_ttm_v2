
def get_routes_to_string(routes):
    names_tuple = []
    for i in routes:
        if i.whereFrom.town not in names_tuple:
            names_tuple.append(i.whereFrom.town)
        if i.whreTo.town not in names_tuple:
            names_tuple.append(i.whreTo.town)
    return " -> ".join(names_tuple)