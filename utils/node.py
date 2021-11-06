from graphene.relay import Node

class CustomNode(Node):  # extends graphene.relay.Node and returns a non-encoded ID
    class Meta:
        name = 'Nodes'
    
    @staticmethod
    def to_global_id(type, id):
        return id