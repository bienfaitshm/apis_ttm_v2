import graphene


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "hello"


class Mutation(graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    pass


types = []

schema = graphene.Schema(query=Query, types=types)
