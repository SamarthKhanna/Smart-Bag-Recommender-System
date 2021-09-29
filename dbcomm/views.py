from django.shortcuts import render
from dbcomm.prediction import SmartBagRecommendations,FrontPage

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from dbcomm.models import User,Products,Orders
from dbcomm.serializer import UserSerializer,PasswordSerializer,ProductSerializer,OrderSerializer
from rest_framework.decorators import api_view
import pandas as pd
from collections import defaultdict

@api_view(['POST'])
def signup_user(request):
    if request.method == 'POST':
        signup_data = JSONParser().parse(request)
        signup_data['email_id'] = signup_data['email']
        signup_serializer =  UserSerializer(data = signup_data)
        if signup_serializer.is_valid():
            signup_serializer.save()
            return JsonResponse(signup_serializer.data,status = status.HTTP_201_CREATED)
        return JsonResponse(signup_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        login = JSONParser().parse(request)
        try:
            user = User.objects.get(email_id = login["email"])
            user = UserSerializer(user)
            #print(user.data["password"],login["password"])
            if user.data["password"] == login["password"]:
                return JsonResponse({'message': 'Successful','user_id':user.data["user_id"]},status = status.HTTP_202_ACCEPTED)
            else:
                return JsonResponse({'message': 'Not authorized'}, status = status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'},status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def products(request,cat):
    if request.method == 'GET':
        pros = Products.objects.filter(major = cat)
        pro_serialized = ProductSerializer(pros,many = True)
        return JsonResponse(pro_serialized.data,safe = False)

@api_view(['GET'])
def products_all(request):
    if request.method == 'GET':
        pros = Products.objects.all()
        pro_serialized = ProductSerializer(pros,many = True)
        return JsonResponse(pro_serialized.data,safe = False)
        
@api_view(['GET'])
def smartbag_products(request,id):
    if request.method == 'GET':
        bag = SmartBagRecommendations(str(id))
        dicts = {}
        for val in bag:
            temp = Products.objects.filter(item_id__in = bag[val])
            pro_serialized = ProductSerializer(temp,many = True)
            print(pro_serialized.data)
            dicts[val] = pro_serialized.data
        print(dicts)
        return JsonResponse(dicts,safe=False)

@api_view(['GET'])
def order_by_user(request,id):
    if request.method == 'GET':
        orders = Orders.objects.filter(user_id = id)
        ord_serialized = OrderSerializer(orders,many = True)
        order_his = group_by_order_id(ord_serialized.data)
        for key in order_his:
            temp = Products.objects.filter(item_id__in = order_his[key]["items_id"])
            pro_serialized = ProductSerializer(temp,many = True)
            order_his[key]["pro_det"] = pro_serialized.data
        return JsonResponse(order_his,safe = False)

@api_view(['GET'])
def load_front_page(request):
    if request.method == 'GET':
        bag = FrontPage()
        dicts = {}
        for val in bag:
            temp = Products.objects.filter(item_id__in = bag[val])
            pro_serialized = ProductSerializer(temp,many = True)
            dicts[val] = pro_serialized.data
        products = Products.objects.all()
        products = ProductSerializer(products,many=True).data
        products = get_pro_by_cat(products)
        print(products)
        front_page = {**products,**dicts}
        return JsonResponse(front_page,safe = False)


def get_pro_by_cat(prods):
    tree = {}
    for prod in prods:
        major = prod['major']
        minor = prod['minor']
        ptype = prod['typeP']
        if major not in tree:
            tree[major] = {}
        if minor not in tree[major]:
            tree[major][minor] = {}
        if ptype not in tree[major][minor]:
            tree[major][minor][ptype] = []
        tree[major][minor][ptype].append(prod)
    return tree      


def group_by_order_id(input_list):
    output_dict = defaultdict(dict)
    for item in input_list:
        if not output_dict[item["order_id"]]:
            output_dict[str(item["order_id"])]['user_id'] = item["user_id"]
            output_dict[str(item["order_id"])]['day_of_month'] = item["day_of_month"]
            output_dict[str(item["order_id"])]['items_id'] = []
        output_dict[str(item["order_id"])]['items_id'].append(item['item_id'])
        #print(output_dict)
    return output_dict


