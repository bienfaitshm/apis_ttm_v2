import graphene
import json
from apps.dash.schema import Query as DashQueries
from apps.clients.schema import Query as ClientQueries, Mutation as ClientMutation

from apps.dash.models import Journey
from utils import trajets


class Query(DashQueries, ClientQueries, graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "hello"


class Mutation(ClientMutation, graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    pass


types = []

schema = graphene.Schema(query=Query, mutation=Mutation, types=types)
