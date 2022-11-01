from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializer import *
from ipware import get_client_ip


@api_view(['POST'])
def wishlist_add(request,):
     ads_id = request.POST['ads_id']
     client_ip, is_routable = get_client_ip(request)
     if client_ip is None:
         return Response({"Unable to get the client's IP address"})
     else:
        Wishlist.objects.create(ip=client_ip, ads_id=ads_id)
        return Response({"added"})


@api_view(['GET'])
def profile(request):
    user = request.user
    ads = Ads.objects.filter(owner_id=user)
    query = AdsSerializer(ads, many=True)
    data = {
        "ads": query.data
    }
    return Response(data)


@api_view(['GET'])
def another_profile(request, pk):
    user = User.objects.get(id=pk)
    query = Ads.objects.filter(owner_id=user)
    ser = UserSerializer(user)
    ads = AdsSerializer(query, many=True)
    data = {
        'user': ser.data,
        'ads': ads.data
    }
    return Response(data)


def category_filter(request, pk):
    cat = Category.objects.get(id=pk)
    sub = Subcategory.objects.get(category_id=cat)
    ads = Ads.objects.filter(category_id=sub)
    return render(request, {'ads': ads})


def subcategory_filter(request, pk):
    cat = Category.objects.get(id=pk)
    sub = Subcategory.objects.filter(category_id=cat)
    return render(request, {'subcategory': sub})


def ads_filter(request, pk):
    cat = Subcategory.objects.get(id=pk)
    ads = Ads.objects.filter(category_id=cat)
    return render(request, {'ads': ads})


@api_view(['POST', 'GET'])
def search_region(request):
    status = request.POST.get('status')
    name = request.POST.get('name')
    price = request.POST.get('price')
    if status == '1':
        region = SubRegion.objects.filter(name__icontains=name)
        ads = Ads.objects.filter(region_id=region.id)
        query = AdsSerializer(ads, many=True)
        data = {
            "ads": query.data
        }
        return Response(data)
    elif status == '2':
        ads = Ads.objects.filter(price__gte=price, price__lte=price)
        query = AdsSerializer(ads, many=True)
        data = {
            "ads": query.data
        }
        return Response(data)
    else:
        return Response('it doesnt work')
