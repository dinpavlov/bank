from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountSerializer, TransferSerializer
from .services import make_transfer


@api_view(['GET'])
def account_get(request, id):
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return Response('Account with id={} does not exist'.format(id),status=status.HTTP_404_NOT_FOUND)
    serializer = AccountSerializer(account)
    return Response({'balance': serializer.data['balance']}, status=status.HTTP_200_OK)

@api_view(['POST'])
def account_create(request):
    data = request.data
    serializer = AccountSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def transfer_create(request):
    data = request.data
    serializer = TransferSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        try:
            make_transfer(**serializer.validated_data)
            return Response({'transfer status': 'Successfull'}, status = status.HTTP_200_OK)
        except ValueError:
            return Response({'transfer status': 'Unsuccessfull'}, status = status.HTTP_400_BAD_REQUEST)
            