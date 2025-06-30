import graphene
from graphene_django.types import DjangoObjectType

class Query(graphene.ObjectType):
    """
    Root query for the GraphQL API.
    """
    hello = graphene.String(default_value="Hello, GraphQL!")

schema = graphene.Schema(query=Query)