from django.db.models import fields
from rest_framework import serializers
from dbcomm.models import User,Products,Orders

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id','email_id','password')
        #extra_kwargs = {'password': {'write_only' : True}}

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password')
        read_only_fields = ('password')

class ProductSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        many = kwargs.pop('many',True)
        super(ProductSerializer,self).__init__(many=many,*args,**kwargs)
            
    class Meta:
        model = Products
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'