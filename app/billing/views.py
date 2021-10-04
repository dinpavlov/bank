from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def account_get(request, id):
    return Response('account_get_endpoint')