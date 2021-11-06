from graphql_jwt.shortcuts import get_user_by_token

class UserMixin:
    @classmethod
    def get_user(cls, info):
        if hasattr(info.context, "query_string"):
            user = get_user_by_token(info.context.query_string, info.context)
            return user
        request = info.context
        return request.user

    @classmethod
    def is_authenticated(cls, info)->bool:        
        return cls.get_user(info) and cls.get_user(info).is_authenticated