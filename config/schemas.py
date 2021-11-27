import graphene
import json
from apps.dash.schema import Query as DashQueries
from apps.clients.schema import Query as ClientQueries, Mutation as ClientMutation

from apps.dash.models import Journey
class Query(DashQueries, ClientQueries, graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        journey = Journey.objects.all()
        for v in journey:
            # print(v.get_journey_routes())
            routes_trajets(v.get_routes())
        # print("seeting", phone_verify_settings)
        return "hello"

def add_dic (values_dict, value, tmp):  
    values_dict[value.pk] = {
        "from ": tmp.whereTo.pk if tmp else None,
        "to": tmp.whereFrom.pk if tmp else None,
        "value" : value,
    }

    

def routes_trajets(routes):
    mydic = {}
    where_from = None
    where_to = None
    tmp = None
    for index, item in enumerate(routes) :
        # add_dic(mydic,item.whereTo, tmp)
        # add_dic(mydic,item.whereFrom, tmp)

        if index > 1:
            if item.whereTo.pk in mydic:
                mydic[item.whereTo.pk]["to"] = item.whereFrom.pk 
                mydic[item.whereTo.pk]["from"] = tmp.whereTo.pk
            else:
                mydic[item.whereTo.pk] = {
                    "from": tmp.whereTo.pk if tmp else None,
                    "to": tmp.whereFrom.pk if tmp else None,
                    "object":item.whereTo
                }

            if item.whereFrom.pk in mydic:
                mydic[item.whereFrom.pk] = {
                    "from": tmp.whereTo.pk if tmp else None,
                    "to": tmp.whereFrom.pk if tmp else None,
                    "object": item.whereFrom
                }
            if tmp.whereFrom.pk == item.whereTo.pk:
                where_from = item.whereFrom
            if tmp.whereTo.pk == item.whereFrom.pk:
                where_to = item.whereTo
        else :
            add_dic(mydic, item.whereTo, tmp)
            add_dic(mydic, item.whereFrom, tmp)
            where_from = item.whereFrom
            where_to = item.whereTo
        tmp = item
        print(item, index,"  from ", where_from," to ", where_to)
    print (json.dumps(mydic, indent=2, default=str))
    print("_______________")
class Mutation(ClientMutation, graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    pass

types = []

schema = graphene.Schema(query=Query, mutation=Mutation, types=types)