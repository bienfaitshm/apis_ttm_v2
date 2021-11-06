import graphene
from apps.dash.schema import Query as DashQueries

class Query(DashQueries, graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        # print("seeting", phone_verify_settings)
        return "hello"


class Mutation(graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    pass

types = []

schema = graphene.Schema(query=Query,  types=types)