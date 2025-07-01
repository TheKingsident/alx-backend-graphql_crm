import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(CRMQuery, graphene.ObjectType):
    """
    Root query for the GraphQL API.
    """
    hello = graphene.String(default_value="Hello, GraphQL!")

    def resolve_hello(self, info):
        return "Hello, GraphQL from CRM!"


class Mutation(CRMMutation, graphene.ObjectType):
    """
    Root mutation for the GraphQL API.
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)