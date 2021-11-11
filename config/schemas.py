import graphene
from apps.dash.schema import Query as DashQueries
from apps.clients.schema import Query as ClientQueries, Mutation as ClientMutation
class Query(DashQueries, ClientQueries, graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        # print("seeting", phone_verify_settings)
        return "hello"


class Mutation(ClientMutation, graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    pass

types = []

schema = graphene.Schema(query=Query, mutation=Mutation, types=types)