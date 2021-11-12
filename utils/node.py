from graphene.relay import Node
from apps.dash import models
class CustomNode(Node):  # extends graphene.relay.Node and returns a non-encoded ID
    class Meta:
        name = 'Nodes'
    
    @classmethod
    def to_global_id(cls, type_, id):
        return id
    
    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        get_node = getattr(only_type, "get_node", None)
        if get_node:
            return get_node(info, global_id)