import random
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate, login
from .serializer import *
from ipware import get_client_ip
from rest_framework.authentication import BasicAuthentication, SessionAuthentication


class Page(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class ads_page(generics.ListAPIView):
    serializer_class = AdsSerializer
    pagination_class = Page
    queryset = Ads.objects.all()


@api_view(['POST'])
def wishlist_add(request,):
     ads_id = request.POST['ads-id']
     client_ip, is_routable = get_client_ip(request)
     if client_ip is None:
         return Response({"Unable to get the client's IP address"})
     else:
        Wishlist.objects.create(ip=client_ip, ads_id=ads_id)
        return Response({"added"})


@api_view(['GET'])
def profile(request):
    user = request.user
    ads = Ads.objects.filter(owner_id=user.id)
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


@api_view(['GET'])
def category_filter(request, pk):
    cat = Category.objects.get(id=pk)
    sub = Subcategory.objects.get(category_id=cat)
    ads = Ads.objects.filter(category_id=sub)
    query = AdsSerializer(ads, many=True)
    data = {
        'ads': query.data
    }
    return Response(data)


@api_view(['GET'])
def subcategory_filter(request, pk):
    cat = Category.objects.get(id=pk)
    sub = Subcategory.objects.filter(category_id=cat)
    query = SubSerializer(sub, many=True)
    data = {
        'sub': query.data
    }
    return Response(data)


@api_view(['GET'])
def ads_filter(request, pk):
    cat = Subcategory.objects.get(id=pk)
    ads = Ads.objects.filter(category_id=cat)
    query = AdsSerializer(ads, many=True)
    data = {
        'ads': query.data
    }
    return Response(data)


@api_view(['GET'])
def search(request):
    status = request.POST.get('status')
    price_bigger = request.POST.get('price-bigger')
    price_smaller = request.POST.get('price-smaller')
    region = request.POST.get('region')
    name = request.POST.get('name')
    if status is not None:
        if status == '1':
            ads = Ads.objects.filter(price__gte=price_smaller, price__lte=price_bigger)
        elif status == '2':
            subregion = SubRegion.objects.get(district__icontains=region)
            ads = Ads.objects.filter(region_id=subregion)
        elif status == '3':
            ads = Ads.objects.filter(name__icontains=name)
        else:
            return Response('something went wrong')
        query = AdsSerializer(ads, many=True)
        data = {
            'ads': query.data
        }
        return Response(data)
    if region is not None:
        subregion = SubRegion.objects.get(district__icontains=region)
        ads = Ads.objects.filter(region_id=subregion)
    elif price_bigger is not None:
        ads = Ads.objects.filter(price__gte=price_smaller, price__lte=price_bigger)
    elif name is not None:
        ads = Ads.objects.filter(name__icontains=name)
    else:
        return Response('something went wrong')
    query = AdsSerializer(ads, many=True)
    data = {
        "ads": query.data
    }
    return Response(data)


@api_view(['GET'])
def statuses(request):
    is_top = []
    is_recommended = []
    for i in Ads.objects.all():
        if i.is_top == True:
            is_top.append(i)
        elif i.is_recommended == True:
            is_recommended.append(i)
    data = {
        'is_top': AdsSerializer(is_top, many=True).data,
        'is_recommended': AdsSerializer(is_recommended, many=True).data,
    }
    return Response(data)


@api_view(['POST'])
def register(request):
    try:
        try:
            number = request.POST.get('number')
            password = request.POST.get('password')
            if number[:3] == '998':
                if len(number) == 12:
                    username = number
                    number = int(number)
                    print(username)
                    usr = User.objects.create_user(username=username, number=number, password=password, status=2)
                    data = {
                        'username': username,
                        'number': number,
                        'user_id': usr.id,
                    }
                    return Response(data)
                return Response('Your number is wrong')
            else:
                return Response('Your email or number is wrong')
        except Exception as err:
            return Response({"error": f'{err}'})
    except Exception as err:
        return Response({"error": f'{err}'})


@api_view(['POST'])
def login_view(request):
    phone = request.POST['phone']
    password = request.POST['password']
    users = User.objects.filter(username=phone)
    if users is not None:
        usr = authenticate(username=phone, password=password)
        if usr is not None:
            login(request, usr)
            return Response('done')
        return Response('User is doesnt exist')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def reset_password(request):
    user = request.user
    last_password = request.POST.get('last-password')
    new_password = request.POST.get('new-password')
    user = authenticate(username=user.username, password=last_password)
    if user is not None:
        user.set_password(new_password)
        user.save()
        return Response('Your password has changed')
    return Response('wrong')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def get_info(request):
    info = Information.objects.last()
    if info is not None:
        query = InfoSerializer(info)
        data = {
            'info': query.data
        }
        return Response(data)
    else:
        return Response('We have not info yet')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def update_ads(request):
    user = request.user
    ads = Ads.objects.filter(owner_id=user)
    if request.method == 'GET':
        if len(ads) == 0:
            return Response('This user have not ads which accepted')
        else:
            das = []
            for i in ads:
                data = {
                    'id': i.id,
                    'name': i.name,
                    'description': i.description,
                    'status': i.status
                }
                das.append(data)
            return Response(das)
    elif request.method == 'POST':
        id_ads = request.POST.get('id')
        region = request.POST.get('region')
        category = request.POST.get('category')
        name = request.POST.get('name')
        photo = request.POST.getlist('photo')
        price = request.POST.get('price')
        description = request.POST.get('description')
        ads = Ads.objects.get(id=id_ads)
        ads.region = region
        ads.category = category
        ads.name = name
        ads.photo = photo
        ads.price = price
        ads.description = description
        ads.save()
    else:
        return Response('You work with wrong method')


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def delete_ads(request):
    user = request.user
    ads = Ads.objects.filter(owner_id=user)
    if request.method == 'GET':
        if len(ads) == 0:
            return Response('This user have not ads which accepted')
        else:
            das = []
            for i in ads:
                data = {
                    'id': i.id,
                    'name': i.name,
                    'description': i.description,
                    'status': i.status
                }
                das.append(data)
            return Response(das)
    elif request.method == 'DELETE':
        id_ads = request.POST.get('id')
        ads_v = Ads.objects.get(id=id_ads)
        ads_v.delete()
        return Response('Your ads has deleted')
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def sale_ads(request):
    if request.method == 'GET':
        user = request.user
        ads = Ads.objects.filter(owner_id=user, status=2)
        if len(ads) == 0:
            return Response('This user have not ads which accepted')
        else:
            das = []
            for i in ads:
                data = {
                    'id': i.id,
                    'name': i.name,
                    'description': i.description,
                    'status': i.status
                }
                das.append(data)
            return Response(das)
    elif request.method == 'POST':
        id_ads = request.POST['id']
        ads_s = Ads.objects.get(id=id_ads)
        ads_s.status = 4
        ads_s.save()
        return Response({'Your Ads successfully has been sold'})
    else:
        return Response({'I think you doing something wrong'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def add_ads_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        AdImage.objects.create(photo=image)
        return Response('done')
    else:
        return Response('something went wrong')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def add_ads(request):
    if request.method == 'POST':
        user = request.user
        region = request.POST.get('region')
        category = request.POST.get('category')
        photo = request.POST.getlist('photo')
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        a = Ads.objects.create(owner_id=user, region_id=region, category_id=category, name=name, price=price, description=description, status=1)
        for i in photo:
            a.student.add(AdImage.objects.get(id=i))
            return Response('done')
        return Response("something went wrong")
    else:
        return Response('You have to give POST method')
