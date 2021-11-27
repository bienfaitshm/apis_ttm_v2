import graphene
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

def routes_trajets(routes):
    where_from = None
    where_to = None
    tmp = None
    for index, item in enumerate(routes) :
        if index > 1:
            if tmp.whereFrom.pk == item.whereTo.pk:
                where_from = item.whereFrom
            if tmp.whereTo.pk == item.whereFrom.pk:
                where_to = item.whereTo
        else :
            where_from = item.whereFrom
            where_to = item.whereTo
        tmp = item
        print(item, index,"  from ", where_from," to ", where_to)
    print("_______________")
class Mutation(ClientMutation, graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    pass

types = []

schema = graphene.Schema(query=Query, mutation=Mutation, types=types)