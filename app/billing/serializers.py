from rest_framework import serializers
from .models import Account



class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        # the author to be automatically the user who is making the request, so it does not need that field to be editable
        read_only_fields = ('user','balance',)